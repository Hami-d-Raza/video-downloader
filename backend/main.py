"""
Video Downloader Backend - FastAPI Application
Supports YouTube, Facebook, Instagram, and TikTok

DISCLAIMER: Users must have rights to download content.
Only supports publicly accessible content.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
import os
import logging
from datetime import datetime, timedelta
import asyncio

from downloader import VideoDownloader
from utils import (
    validate_url,
    detect_platform,
    is_playlist_url,
    cleanup_old_files,
    rate_limiter
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Video Downloader API",
    description="Download videos from YouTube, Facebook, Instagram, and TikTok",
    version="1.0.0"
)

# CORS middleware
# Get allowed origins from environment variable or use defaults
allowed_origins_str = os.getenv("FRONTEND_URL", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

# Add localhost variants for development
development_origins = ["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"]
for dev_origin in development_origins:
    if dev_origin not in allowed_origins:
        allowed_origins.append(dev_origin)

# For Railway deployments, allow Railway domains
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Allow all Railway.app domains in Railway environment
    allow_origin_regex = r"https://.*\.up\.railway\.app"
else:
    allow_origin_regex = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create downloads directory
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Initialize downloader
downloader = VideoDownloader(DOWNLOAD_DIR)

# Request models
class AnalyzeRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    format_id: Optional[str] = None
    quality: Optional[str] = "best"
    audio_only: bool = False

class BatchDownloadRequest(BaseModel):
    urls: List[str]
    format_id: Optional[str] = None
    quality: Optional[str] = "best"
    audio_only: bool = False

# Response models
class FormatInfo(BaseModel):
    format_id: str
    quality: str
    ext: str
    filesize: Optional[int] = None
    filesize_str: Optional[str] = None
    format_note: Optional[str] = None

class AnalyzeResponse(BaseModel):
    title: str
    thumbnail: str
    duration: int
    duration_str: str
    platform: str
    formats: List[FormatInfo]
    uploader: Optional[str] = None
    view_count: Optional[int] = None

class DownloadResponse(BaseModel):
    status: str
    message: str
    filename: Optional[str] = None
    download_url: Optional[str] = None

class BatchDownloadResponse(BaseModel):
    status: str
    message: str
    filename: Optional[str] = None  # ZIP filename
    download_url: Optional[str] = None
    total_videos: int
    successful: int
    failed: int

class PlaylistVideoInfo(BaseModel):
    id: str
    title: str
    url: str
    duration: Optional[int] = None
    duration_str: Optional[str] = None
    thumbnail: Optional[str] = None

class PlaylistResponse(BaseModel):
    title: str
    platform: str
    video_count: int
    videos: List[PlaylistVideoInfo]
    uploader: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Cleanup old files on startup"""
    logger.info("Starting Video Downloader API")
    cleanup_old_files(DOWNLOAD_DIR, hours=1)  # Delete files older than 1 hour


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Video Downloader API is running",
        "supported_platforms": ["YouTube", "Facebook", "Instagram", "TikTok"],
        "disclaimer": "Users must have rights to download content. Only publicly accessible content is supported."
    }


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_video(request: AnalyzeRequest):
    """
    Analyze a video URL and return available formats
    
    Args:
        request: Contains the video URL
        
    Returns:
        Video metadata including title, thumbnail, duration, and available formats
    """
    try:
        # Rate limiting check
        if not rate_limiter.check_rate_limit(request.url):
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
        
        # Validate URL
        if not validate_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Detect platform
        platform = detect_platform(request.url)
        if not platform:
            raise HTTPException(
                status_code=400,
                detail="Unsupported platform. Only YouTube, Facebook, Instagram, and TikTok are supported."
            )
        
        logger.info(f"Analyzing {platform} video: {request.url}")
        
        # Get video info
        info = await downloader.get_video_info(request.url)
        
        if not info:
            raise HTTPException(status_code=404, detail="Could not retrieve video information")
        
        logger.info(f"Successfully retrieved info for {platform}: {info.get('title', 'Unknown')[:50]}")
        logger.info(f"Available metadata fields: {list(info.keys())[:20]}")
        
        # Format duration
        duration = info.get('duration', 0) or 0
        # Convert to int to handle float durations from some platforms
        duration = int(duration) if duration else 0
        duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
        
        # Extract simplified quality options
        formats = []
        
        # Define standard quality options that will work with merged video+audio
        quality_options = [
            {"id": "2160p", "label": "4K (2160p)", "height": 2160, "min": 1800, "max": 2400},
            {"id": "1440p", "label": "2K (1440p)", "height": 1440, "min": 1200, "max": 1799},
            {"id": "1080p", "label": "Full HD (1080p)", "height": 1080, "min": 900, "max": 1199},
            {"id": "720p", "label": "HD (720p)", "height": 720, "min": 600, "max": 899},
            {"id": "480p", "label": "SD (480p)", "height": 480, "min": 400, "max": 599},
            {"id": "360p", "label": "Low (360p)", "height": 360, "min": 200, "max": 399},
        ]
        
        # Collect all available heights from formats
        available_heights = set()
        has_video_formats = False
        
        for fmt in info.get('formats', []):
            # Check if format has video (not audio-only)
            if fmt.get('vcodec') and fmt.get('vcodec') != 'none':
                has_video_formats = True
                height = fmt.get('height')
                if height and isinstance(height, (int, float)):
                    available_heights.add(int(height))
        
        logger.info(f"Available heights for {platform}: {sorted(available_heights, reverse=True)}")
        
        # Match available heights to standard quality options
        matched_qualities = set()
        for height in available_heights:
            for quality in quality_options:
                # Use range matching for flexibility
                if quality['min'] <= height <= quality['max']:
                    if quality['id'] not in matched_qualities:
                        formats.append(FormatInfo(
                            format_id=quality['id'],
                            quality=quality['label'],
                            ext="mp4",
                            filesize=None,
                            filesize_str="Varies by quality",
                            format_note="Video + Audio"
                        ))
                        matched_qualities.add(quality['id'])
                    break
        
        # If we found video formats but no standard qualities matched, add best option
        if has_video_formats and not formats:
            formats.append(FormatInfo(
                format_id="best",
                quality="Best Available Quality",
                ext="mp4",
                filesize=None,
                filesize_str=None,
                format_note="Video + Audio"
            ))
        
        # If no video formats at all, still add best option
        if not has_video_formats:
            formats.append(FormatInfo(
                format_id="best",
                quality="Best Available Quality",
                ext="mp4",
                filesize=None,
                filesize_str=None,
                format_note="Video + Audio"
            ))
        
        # Add audio-only option
        formats.append(FormatInfo(
            format_id="audio",
            quality="Audio Only (MP3)",
            ext="mp3",
            filesize=None,
            filesize_str=None,
            format_note="Best audio quality"
        ))
        
        # Extract thumbnail URL with fallbacks
        thumbnail_url = ''
        
        # Try different methods to get thumbnail
        # Method 1: Direct thumbnail field
        if info.get('thumbnail'):
            thumbnail_url = info.get('thumbnail')
        
        # Method 2: Thumbnails array (get highest quality)
        elif info.get('thumbnails') and isinstance(info.get('thumbnails'), list):
            thumbnails = info.get('thumbnails')
            if thumbnails:
                # Filter valid thumbnails with URLs
                valid_thumbs = [t for t in thumbnails if t.get('url')]
                if valid_thumbs:
                    # Try to get the best quality (prefer https)
                    https_thumbs = [t for t in valid_thumbs if t.get('url', '').startswith('https')]
                    if https_thumbs:
                        # Get the one with highest resolution or last in list
                        best_thumb = max(https_thumbs, key=lambda x: (x.get('width', 0), x.get('height', 0)))
                        thumbnail_url = best_thumb.get('url')
                    else:
                        # Fallback to any thumbnail
                        thumbnail_url = valid_thumbs[-1].get('url')
        
        # Method 3: Other thumbnail fields
        if not thumbnail_url:
            thumbnail_url = info.get('thumbnail_url', '')
        
        # Method 4: Platform-specific fallbacks
        if not thumbnail_url:
            # For YouTube, construct thumbnail URL from video ID
            if platform == 'YouTube' and info.get('id'):
                video_id = info.get('id')
                thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
            # For Instagram, try the display_url
            elif platform == 'Instagram':
                thumbnail_url = info.get('display_url', '')
        
        logger.info(f"Thumbnail URL for {platform}: {thumbnail_url[:100] if thumbnail_url else 'None'}")
        
        return AnalyzeResponse(
            title=info.get('title', 'Unknown'),
            thumbnail=thumbnail_url or '',
            duration=duration,
            duration_str=duration_str,
            platform=platform,
            formats=formats,
            uploader=info.get('uploader'),
            view_count=info.get('view_count')
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing video: {str(e)}")


@app.post("/api/analyze-playlist", response_model=PlaylistResponse)
async def analyze_playlist(request: AnalyzeRequest):
    """
    Analyze a YouTube playlist URL and return video list
    
    Args:
        request: Contains the playlist URL
        
    Returns:
        Playlist metadata including title and video entries
    """
    try:
        # Rate limiting check
        if not rate_limiter.check_rate_limit(request.url):
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
        
        # Validate URL
        if not validate_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Check if it's a playlist URL
        if not is_playlist_url(request.url):
            raise HTTPException(status_code=400, detail="Not a valid playlist URL")
        
        # Detect platform
        platform = detect_platform(request.url)
        if platform != 'YouTube':
            raise HTTPException(
                status_code=400,
                detail="Currently only YouTube playlists are supported."
            )
        
        logger.info(f"Analyzing playlist: {request.url}")
        
        # Get playlist info
        info = await downloader.get_playlist_info(request.url)
        
        if not info:
            raise HTTPException(status_code=404, detail="Could not retrieve playlist information")
        
        # Extract video entries
        videos = []
        entries = info.get('entries', [])
        
        logger.info(f"Found {len(entries)} videos in playlist")
        
        for entry in entries:
            if entry:
                duration = entry.get('duration', 0) or 0
                duration_str = f"{int(duration) // 60}:{int(duration) % 60:02d}" if duration else "Unknown"
                
                videos.append(PlaylistVideoInfo(
                    id=entry.get('id', ''),
                    title=entry.get('title', 'Unknown'),
                    url=entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}",
                    duration=int(duration) if duration else None,
                    duration_str=duration_str,
                    thumbnail=entry.get('thumbnail', '')
                ))
        
        return PlaylistResponse(
            title=info.get('title', 'Unknown Playlist'),
            platform=platform,
            video_count=len(videos),
            videos=videos,
            uploader=info.get('uploader')
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing playlist: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing playlist: {str(e)}")


@app.post("/api/download", response_model=DownloadResponse)
async def download_video(request: DownloadRequest, background_tasks: BackgroundTasks):
    """
    Download a video in the specified format
    
    Args:
        request: Contains URL, format_id, quality, and audio_only flag
        background_tasks: FastAPI background tasks for cleanup
        
    Returns:
        Download status and file information
    """
    try:
        # Rate limiting check
        if not rate_limiter.check_rate_limit(request.url):
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
        
        # Validate URL
        if not validate_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Detect platform
        platform = detect_platform(request.url)
        if not platform:
            raise HTTPException(
                status_code=400,
                detail="Unsupported platform. Only YouTube, Facebook, Instagram, and TikTok are supported."
            )
        
        logger.info(f"Downloading {platform} video: {request.url}")
        logger.info(f"Format: {request.format_id}, Audio only: {request.audio_only}")
        
        # Download video
        result = await downloader.download_video(
            url=request.url,
            format_id=request.format_id,
            audio_only=request.audio_only
        )
        
        if not result:
            logger.error("Download returned None")
            raise HTTPException(status_code=500, detail="Download failed. Please try again.")
        
        if 'filepath' not in result:
            logger.error(f"Download result missing filepath: {result}")
            raise HTTPException(status_code=500, detail="Download failed. File not found.")
        
        filepath = result['filepath']
        
        if not os.path.exists(filepath):
            logger.error(f"File does not exist: {filepath}")
            raise HTTPException(status_code=500, detail="Download failed. File not found.")
        
        filename = os.path.basename(filepath)
        logger.info(f"Download successful: {filename}")
        
        # Schedule file deletion after 1 hour
        background_tasks.add_task(delete_file_after_delay, filepath, delay_hours=1)
        
        return DownloadResponse(
            status="success",
            message="Video downloaded successfully",
            filename=filename,
            download_url=f"/api/file/{filename}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")


@app.post("/api/download-batch", response_model=BatchDownloadResponse)
async def download_batch(request: BatchDownloadRequest, background_tasks: BackgroundTasks):
    """
    Download multiple videos and package them into a ZIP file
    
    Args:
        request: Contains list of URLs, format_id, quality, and audio_only flag
        background_tasks: FastAPI background tasks for cleanup
        
    Returns:
        Download status, ZIP file information, and statistics
    """
    try:
        # Validate all URLs
        for url in request.urls:
            if not validate_url(url):
                raise HTTPException(status_code=400, detail=f"Invalid URL format: {url}")
        
        # Limit number of videos to prevent abuse
        if len(request.urls) > 20:
            raise HTTPException(status_code=400, detail="Maximum 20 videos per batch download")
        
        if len(request.urls) == 0:
            raise HTTPException(status_code=400, detail="No URLs provided")
        
        logger.info(f"Starting batch download of {len(request.urls)} videos")
        logger.info(f"Format: {request.format_id}, Audio only: {request.audio_only}")
        
        # Download all videos and create ZIP
        result = await downloader.download_batch(
            urls=request.urls,
            format_id=request.format_id,
            audio_only=request.audio_only
        )
        
        if not result:
            logger.error("Batch download returned None")
            raise HTTPException(status_code=500, detail="Batch download failed. Please try again.")
        
        if 'filepath' not in result:
            logger.error(f"Batch download result missing filepath: {result}")
            raise HTTPException(status_code=500, detail="Batch download failed. ZIP file not created.")
        
        filepath = result['filepath']
        
        if not os.path.exists(filepath):
            logger.error(f"ZIP file does not exist: {filepath}")
            raise HTTPException(status_code=500, detail="Batch download failed. ZIP file not found.")
        
        filename = os.path.basename(filepath)
        logger.info(f"Batch download successful: {filename}")
        logger.info(f"Statistics - Total: {result['total']}, Successful: {result['successful']}, Failed: {result['failed']}")
        
        # Schedule ZIP file deletion after 1 hour
        background_tasks.add_task(delete_file_after_delay, filepath, delay_hours=1)
        
        return BatchDownloadResponse(
            status="success",
            message=f"Downloaded {result['successful']} of {result['total']} videos successfully",
            filename=filename,
            download_url=f"/api/file/{filename}",
            total_videos=result['total'],
            successful=result['successful'],
            failed=result['failed']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch download: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in batch download: {str(e)}")


@app.get("/api/file/{filename}")
async def get_file(filename: str, background_tasks: BackgroundTasks):
    """
    Serve the downloaded file
    
    Args:
        filename: Name of the file to download
        background_tasks: FastAPI background tasks for cleanup
        
    Returns:
        File response
    """
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete file after sending
    background_tasks.add_task(delete_file_after_delay, filepath, delay_hours=0.05)  # ~3 minutes
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='application/octet-stream'
    )


async def delete_file_after_delay(filepath: str, delay_hours: float):
    """Delete a file after a specified delay"""
    await asyncio.sleep(delay_hours * 3600)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Deleted file: {filepath}")
    except Exception as e:
        logger.error(f"Error deleting file {filepath}: {e}")


@app.delete("/api/cleanup")
async def manual_cleanup():
    """Manually trigger cleanup of old files"""
    try:
        deleted_count = cleanup_old_files(DOWNLOAD_DIR, hours=1)
        return {
            "status": "success",
            "message": f"Cleaned up {deleted_count} old files"
        }
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        raise HTTPException(status_code=500, detail="Cleanup failed")


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

