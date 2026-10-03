from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI(
    title="Stream Extractor API",
    description="High-performance media stream extraction API powered by yt-dlp",
    version="1.0.0"
)

# Enable CORS for web and mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Stream Extractor API",
        "endpoints": {
            "/extract?url={video_url}": "Extract direct stream links and formats",
            "/health": "Health check status"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/extract")
def extract_stream(
    url: str = Query(..., description="Target video URL or embed page URL")
):
    """
    Extracts stream URLs, resolutions, and subtitles from any supported video or embed URL.
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        'socket_timeout': 15,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise HTTPException(status_code=404, detail="No video stream found for the provided URL.")

            # Filter and parse playable formats
            formats = []
            for f in info.get("formats", []):
                stream_url = f.get("url")
                if not stream_url:
                    continue

                resolution = f.get("resolution") or (f"{f.get('width')}x{f.get('height')}" if f.get("width") else None)
                quality = f.get("format_note") or resolution or "auto"
                is_m3u8 = "m3u8" in stream_url or f.get("protocol") in ["m3u8", "m3u8_native"]

                formats.append({
                    "format_id": f.get("format_id"),
                    "quality": quality,
                    "resolution": resolution,
                    "ext": f.get("ext"),
                    "url": stream_url,
                    "is_m3u8": is_m3u8,
                    "tbr": f.get("tbr"),
                    "vcodec": f.get("vcodec"),
                    "acodec": f.get("acodec"),
                })

            # Subtitles if available
            subtitles = []
            for lang, subs in info.get("subtitles", {}).items():
                for sub in subs:
                    subtitles.append({
                        "language": lang,
                        "ext": sub.get("ext"),
                        "url": sub.get("url")
                    })

            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "extractor": info.get("extractor"),
                "best_stream_url": info.get("url"),
                "is_m3u8": "m3u8" in (info.get("url") or ""),
                "formats": formats,
                "subtitles": subtitles
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
