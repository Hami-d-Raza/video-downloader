# Instagram Quality Selection

## Overview
Instagram videos now support quality selection, allowing users to choose from available video qualities when downloading.

## How It Works

### 1. Video Analysis
When a user submits an Instagram URL:
- The backend extracts available video formats using yt-dlp
- Detects all available video heights (e.g., 1080p, 720p, 480p)
- Maps them to standard quality options
- Returns the list to the frontend

### 2. Quality Selection
Users can select from:
- **4K (2160p)** - If available
- **2K (1440p)** - If available  
- **Full HD (1080p)** - Most common
- **HD (720p)** - Most common
- **SD (480p)** - Lower quality
- **Low (360p)** - Lowest quality
- **Audio Only (MP3)** - Audio extraction
- **Best Available** - Default/fallback option

### 3. Download Process
When downloading with a specific quality:
- The backend uses yt-dlp's format selection
- Selects the best format at or below the requested height
- Falls back to best available if exact match isn't found

## Technical Details

### Backend Implementation

**In `downloader.py`:**
```python
if is_instagram and not audio_only:
    if format_id and format_id != 'best':
        height = format_id.replace('p', '')
        height_int = int(height)
        ydl_opts['format'] = f'bestvideo[height<={height_int}]+bestaudio/best[height<={height_int}]/best'
    else:
        ydl_opts['format'] = 'best'
```

**In `main.py`:**
- Quality detection works the same for all platforms
- Extracts available heights from format metadata
- Matches to standard quality options using height ranges

### Format Selection Strategy

For Instagram, the format selector uses:
1. `bestvideo[height<=X]+bestaudio` - Preferred: separate video/audio streams
2. `best[height<=X]` - Fallback: combined stream at requested quality
3. `best` - Final fallback: best available quality

### Instagram Limitations

- Instagram typically provides 2-3 quality options (usually 720p and 480p)
- Not all videos have multiple qualities (depends on original upload)
- Private accounts/videos require authentication (not supported)
- Story videos may have limited quality options

## Testing

Run the test script to verify functionality:

```bash
cd backend
python test_instagram.py
```

The test will:
1. Accept an Instagram video URL
2. Display available formats and heights
3. Optionally test downloading with quality selection

## API Usage

### Analyze Video
```bash
POST /api/analyze
{
  "url": "https://www.instagram.com/p/..."
}
```

Returns available formats including quality options.

### Download Video
```bash
POST /api/download
{
  "url": "https://www.instagram.com/p/...",
  "format_id": "720p",  # or "480p", "1080p", "best", etc.
  "audio_only": false
}
```

## Troubleshooting

### No Quality Options Shown
- Video might be a photo post (no video)
- Private account (requires authentication)
- Network/API issues

### Download Fails with Specific Quality
- Requested quality might not be available
- Try "best" or a lower quality
- Check backend logs for details

### Only "Best Available" Option
- Instagram only provided one quality level
- Original video was uploaded in single quality
- This is normal for some posts

## Future Enhancements

Potential improvements:
- Cookie-based authentication for private accounts
- Story video support
- Carousel/album download support
- Better quality detection for Reels
