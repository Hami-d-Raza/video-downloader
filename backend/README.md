# Video Downloader Backend

FastAPI backend for downloading videos from YouTube, Facebook, Instagram, and TikTok.

## Features

- ✅ Multi-platform support (YouTube, Facebook, Instagram, TikTok)
- ✅ Multiple video quality options
- ✅ Audio-only download (MP3)
- ✅ Automatic format detection
- ✅ Rate limiting
- ✅ Auto file cleanup
- ✅ Error handling

## Prerequisites

- Python 3.8+
- FFmpeg (required for video/audio processing)

### Installing FFmpeg

**Windows:**
```powershell
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## Installation

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:

**Windows:**
```powershell
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file:
```bash
cp .env.example .env
```

## Running the Server

### Development
```bash
python main.py
```

The server will start at `http://localhost:8000`

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### GET /
Health check endpoint

### POST /api/analyze
Analyze a video URL and get metadata

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

**Response:**
```json
{
  "title": "Video Title",
  "thumbnail": "https://...",
  "duration": 180,
  "duration_str": "3:00",
  "platform": "YouTube",
  "formats": [
    {
      "format_id": "137",
      "quality": "1080p",
      "ext": "mp4",
      "filesize": 12345678,
      "filesize_str": "11.77 MB"
    }
  ],
  "uploader": "Channel Name",
  "view_count": 1000000
}
```

### POST /api/download
Download a video in specified format

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "format_id": "137",
  "audio_only": false
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Video downloaded successfully",
  "filename": "video_file.mp4",
  "download_url": "/api/file/video_file.mp4"
}
```

### GET /api/file/{filename}
Download the file

## Configuration

Edit `.env` file:

```env
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
MAX_FILE_AGE_HOURS=1
DOWNLOAD_DIR=./downloads
MAX_REQUESTS_PER_MINUTE=20
```

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── downloader.py        # Video downloader module
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── downloads/           # Downloaded files (auto-created)
```

## Rate Limiting

Default: 20 requests per minute per IP/URL combination

## File Cleanup

Downloaded files are automatically deleted:
- After 1 hour by default
- After being served to the user
- On server startup (old files)

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `400` - Invalid request
- `404` - Not found
- `429` - Rate limit exceeded
- `500` - Server error

## Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **yt-dlp** - Video downloader
- **pydantic** - Data validation
- **aiofiles** - Async file operations

## Security Notes

⚠️ **Important:**
- Only publicly accessible content is supported
- Users must have rights to download content
- Rate limiting prevents abuse
- Files are auto-deleted to save storage
- Input validation prevents malicious URLs

## Troubleshooting

### yt-dlp errors
```bash
# Update yt-dlp
pip install --upgrade yt-dlp
```

### FFmpeg not found
Make sure FFmpeg is installed and in your PATH

### Port already in use
Change PORT in `.env` file or:
```bash
uvicorn main:app --port 8001
```

## License

For educational purposes only. Respect copyright and platform terms of service.
