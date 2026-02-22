"""
Video Downloader Module
Uses yt-dlp to download videos from various platforms
"""

import os
import logging
from typing import Optional, Dict, Any, List
import yt_dlp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import zipfile
from datetime import datetime

logger = logging.getLogger(__name__)


class VideoDownloader:
    """Handle video downloading using yt-dlp"""
    
    def __init__(self, download_dir: str):
        """
        Initialize the downloader
        
        Args:
            download_dir: Directory to save downloaded files
        """
        self.download_dir = download_dir
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Base yt-dlp options
        self.base_opts = {
            'outtmpl': os.path.join(download_dir, '%(title)s_%(id)s.%(ext)s'),
            'restrictfilenames': True,  # Restrict filenames to ASCII
            'no_warnings': False,
            'ignoreerrors': False,
            'extract_flat': False,
            'quiet': False,
            'no_color': True,
            # Cookie and authentication options
            'cookiefile': None,
            'username': None,
            'password': None,
            # Instagram-specific extractor arguments
            'extractor_args': {
                'instagram': {
                    'include_ondemand_in_playlists': ['true']
                }
            },
            # Add headers to avoid blocking (especially for Instagram)
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
        }
    
    async def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get video/post information without downloading
        
        Args:
            url: Video or post URL
            
        Returns:
            Dictionary containing media metadata
        """
        try:
            ydl_opts = {
                **self.base_opts,
                'skip_download': True,  # Don't download, just get info
                'format': 'best',
                'writethumbnail': False,  # We just need the URL, not the file
                'writesubtitles': False,
                'writeautomaticsub': False,
                # Additional options for better metadata extraction
                'extract_flat': False,
                # Don't restrict to single items - allows carousel/image posts
                'no_playlist': False,
                # For Instagram, we need to allow image-only posts
                'ignoreerrors': False,
            }
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(
                self.executor,
                self._extract_info,
                url,
                ydl_opts
            )
            
            # If info is None but it might be an Instagram image post, try to get basic info
            if not info:
                logger.warning("No info extracted, might be an unsupported post type")
            
            return info
        
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    def _extract_info(self, url: str, ydl_opts: dict) -> Optional[Dict[str, Any]]:
        """
        Extract video/post information (runs in thread pool)
        
        Args:
            url: Video or post URL
            ydl_opts: yt-dlp options
            
        Returns:
            Media information dictionary
        """
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"yt-dlp extraction error: {e}")
            raise
    
    async def download_video(
        self,
        url: str,
        format_id: Optional[str] = None,
        audio_only: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Download a video
        
        Args:
            url: Video URL
            format_id: Specific format ID to download
            audio_only: If True, download audio only and convert to MP3
            
        Returns:
            Dictionary with download result including filepath
        """
        try:
            ydl_opts = self.base_opts.copy()
            
            if audio_only:
                # Audio only - extract and convert to MP3
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(self.download_dir, '%(title)s_%(id)s.%(ext)s'),
                })
            elif format_id and format_id != 'best':
                # Specific quality requested - always merge video + audio
                # Extract height from format_id (e.g., "1080p" -> 1080)
                height = format_id.replace('p', '')
                
                # Try multiple format selection strategies for maximum compatibility
                # 1. Try exact height with preferred containers
                # 2. Try height range (±100px) for flexibility
                # 3. Fall back to best available at or below requested height
                height_int = int(height)
                height_min = height_int - 100
                height_max = height_int + 50
                
                format_selectors = [
                    # Prefer mp4/m4a containers
                    f'bestvideo[height>={height_min}][height<={height_max}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height>={height_min}][height<={height_max}]+bestaudio',
                    # Try exact or lower height
                    f'bestvideo[height<={height_int}]+bestaudio/best[height<={height_int}]',
                    # Final fallback to best available
                    'bestvideo+bestaudio/best'
                ]
                
                ydl_opts['format'] = '/'.join(format_selectors)
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]
                
                logger.info(f"Format selector for {height}p: {ydl_opts['format']}")
            else:
                # Best quality video + audio
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]
            
            # Run download in executor
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._download,
                url,
                ydl_opts
            )
            
            if not result:
                logger.error("Download executor returned None")
                return None
            
            logger.info(f"Download completed successfully: {result.get('filepath', 'unknown')}")
            return result
        
        except Exception as e:
            logger.error(f"Error downloading video: {e}", exc_info=True)
            return None
    
    def _download(self, url: str, ydl_opts: dict) -> Optional[Dict[str, Any]]:
        """
        Download video (runs in thread pool)
        
        Args:
            url: Video URL
            ydl_opts: yt-dlp options
            
        Returns:
            Download result dictionary
        """
        try:
            import time
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the expected filename
                filename = ydl.prepare_filename(info)
                base_path, _ = os.path.splitext(filename)
                
                # Wait a moment for post-processing to complete
                time.sleep(1)
                
                # Determine actual filepath after post-processing
                filepath = None
                
                # Check for post-processed files
                if ydl_opts.get('postprocessors'):
                    for pp in ydl_opts['postprocessors']:
                        if pp.get('key') == 'FFmpegExtractAudio':
                            # Audio extraction - check for mp3
                            mp3_path = f"{base_path}.mp3"
                            if os.path.exists(mp3_path):
                                filepath = mp3_path
                                break
                        elif pp.get('key') == 'FFmpegVideoConvertor':
                            # Video conversion - check for mp4
                            mp4_path = f"{base_path}.mp4"
                            if os.path.exists(mp4_path):
                                filepath = mp4_path
                                break
                
                # If not found via post-processors, try the original filename
                if not filepath and os.path.exists(filename):
                    filepath = filename
                
                # Last resort: check for common extensions in the directory
                if not filepath:
                    for ext in ['.mp4', '.mp3', '.webm', '.mkv', '.m4a']:
                        try_path = base_path + ext
                        if os.path.exists(try_path):
                            filepath = try_path
                            break
                
                # Final check: look for the most recent file in downloads directory
                if not filepath:
                    download_dir = os.path.dirname(filename)
                    if os.path.exists(download_dir):
                        files = [
                            os.path.join(download_dir, f) 
                            for f in os.listdir(download_dir) 
                            if os.path.isfile(os.path.join(download_dir, f))
                        ]
                        if files:
                            # Get most recently modified file
                            most_recent = max(files, key=os.path.getmtime)
                            # Check if it was created in the last 120 seconds
                            if time.time() - os.path.getmtime(most_recent) < 120:
                                filepath = most_recent
                                logger.info(f"Found recent file: {filepath}")
                
                if not filepath or not os.path.exists(filepath):
                    logger.error(f"Downloaded file not found. Expected: {filename}")
                    logger.error(f"Checked paths: {base_path}.mp4, {base_path}.mp3, etc.")
                    # List actual files in directory for debugging
                    download_dir = os.path.dirname(filename)
                    if os.path.exists(download_dir):
                        actual_files = os.listdir(download_dir)
                        logger.error(f"Files in directory: {actual_files}")
                    return None
                
                logger.info(f"Successfully located file: {filepath}")
                
                return {
                    'filepath': filepath,
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'filesize': os.path.getsize(filepath) if os.path.exists(filepath) else 0
                }
        
        except Exception as e:
            logger.error(f"yt-dlp download error: {e}")
            raise
    
    async def get_playlist_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get playlist information
        
        Args:
            url: Playlist URL
            
        Returns:
            Dictionary containing playlist metadata and video entries
        """
        try:
            ydl_opts = {
                **self.base_opts,
                'skip_download': True,
                'extract_flat': 'in_playlist',  # Get playlist info without downloading
                'playlistend': 50,  # Limit to first 50 videos for performance
            }
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(
                self.executor,
                self._extract_info,
                url,
                ydl_opts
            )
            
            return info
        
        except Exception as e:
            logger.error(f"Error getting playlist info: {e}")
            return None

    async def download_batch(self, urls: List[str], format_id: Optional[str] = None, audio_only: bool = False) -> Optional[Dict[str, Any]]:
        """
        Download multiple videos and package them into a ZIP file
        
        Args:
            urls: List of video URLs to download
            format_id: Format ID for video quality (e.g., '1080p', '720p')
            audio_only: If True, download only audio
            
        Returns:
            Dictionary containing ZIP file path and download statistics
        """
        try:
            downloaded_files = []
            failed_count = 0
            
            logger.info(f"Starting batch download of {len(urls)} videos")
            
            # Download each video
            for idx, url in enumerate(urls, 1):
                try:
                    logger.info(f"Downloading video {idx}/{len(urls)}: {url}")
                    result = await self.download_video(url, format_id, audio_only)
                    
                    if result and 'filepath' in result:
                        filepath = result['filepath']
                        if os.path.exists(filepath):
                            downloaded_files.append(filepath)
                            logger.info(f"Successfully downloaded {idx}/{len(urls)}: {os.path.basename(filepath)}")
                        else:
                            logger.error(f"File not found after download: {filepath}")
                            failed_count += 1
                    else:
                        logger.error(f"Failed to download video {idx}/{len(urls)}")
                        failed_count += 1
                        
                except Exception as e:
                    logger.error(f"Error downloading video {idx}/{len(urls)}: {e}")
                    failed_count += 1
            
            if not downloaded_files:
                logger.error("No videos were successfully downloaded")
                return None
            
            # Create ZIP file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"videos_batch_{timestamp}.zip"
            zip_filepath = os.path.join(self.download_dir, zip_filename)
            
            logger.info(f"Creating ZIP file: {zip_filename}")
            
            with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for filepath in downloaded_files:
                    # Add file to ZIP with just the filename (no path)
                    arcname = os.path.basename(filepath)
                    zipf.write(filepath, arcname)
                    logger.info(f"Added to ZIP: {arcname}")
                    
                    # Delete original file after adding to ZIP
                    try:
                        os.remove(filepath)
                        logger.info(f"Deleted original file: {filepath}")
                    except Exception as e:
                        logger.warning(f"Failed to delete original file {filepath}: {e}")
            
            logger.info(f"Batch download complete. ZIP created: {zip_filename}")
            
            return {
                'filepath': zip_filepath,
                'filename': zip_filename,
                'total': len(urls),
                'successful': len(downloaded_files),
                'failed': failed_count
            }
            
        except Exception as e:
            logger.error(f"Error in batch download: {e}", exc_info=True)
            return None

