# Stream Extractor API (Powered by yt-dlp)

A production-ready FastAPI microservice for extracting direct video streams (`.m3u8` and `.mp4`), resolutions, and subtitles from 1,750+ supported video hosts.

---

## 🚀 How to Host on Render (Step-by-Step)

### Option 1: Automatic Blueprint (1-Click)
1. Push this `extractor-api` folder to a GitHub repository.
2. In your [Render Dashboard](https://dashboard.render.com/), click **New + > Blueprint**.
3. Select your repository. Render will automatically read [`render.yaml`](./render.yaml) and configure:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Click **Apply**. Render will deploy it and give you a public URL (e.g. `https://stream-extractor-api.onrender.com`).

---

### Option 2: Manual Web Service
1. In the [Render Dashboard](https://dashboard.render.com/), click **New + > Web Service**.
2. Connect your GitHub repository.
3. Configure:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`
4. Click **Create Web Service**.

---

## 📡 API Endpoints

### 1. Extract Stream
```http
GET /extract?url={video_or_embed_url}
```

**Example Request:**
```bash
curl "https://your-api.onrender.com/extract?url=https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
```

**Example JSON Response:**
```json
{
  "title": "Sample Stream",
  "duration": 634,
  "thumbnail": "https://...",
  "extractor": "generic",
  "best_stream_url": "https://test-streams.mux.dev/.../1080p.m3u8",
  "is_m3u8": true,
  "formats": [
    {
      "quality": "1080p",
      "resolution": "1920x1080",
      "url": "https://.../1080p.m3u8",
      "is_m3u8": true
    },
    {
      "quality": "720p",
      "resolution": "1280x720",
      "url": "https://.../720p.m3u8",
      "is_m3u8": true
    }
  ],
  "subtitles": []
}
```

### 2. Interactive Swagger Docs
Open `https://your-api.onrender.com/docs` in your browser to test endpoints interactively.

### 3. Health Check
```http
GET /health
```
Returns `{"status": "healthy"}` for uptime monitors.

---

## 💻 Running Locally

```bash
cd extractor-api
pip install -r requirements.txt
python main.py
```
Server runs at `http://localhost:8000`.
