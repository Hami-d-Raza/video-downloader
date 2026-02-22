"""
Test the actual downloader class to reproduce the issue
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from downloader import VideoDownloader


async def test_downloader():
    """Test the actual VideoDownloader class"""
    
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    test_urls = [
        ("YouTube", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        ("Instagram", "https://www.instagram.com/p/C3sS8KLt-3W/"),  # Example, may not work
    ]
    
    for platform, url in test_urls:
        print(f"\n{'=' * 60}")
        print(f"Testing {platform}: {url}")
        print('=' * 60)
        
        try:
            info = await downloader.get_video_info(url)
            
            if info:
                print(f"[SUCCESS!]")
                print(f"  Title: {info.get('title', 'N/A')[:60]}")
                print(f"  Duration: {info.get('duration', 'N/A')}")
                print(f"  Formats available: {len(info.get('formats', []))}")
            else:
                print(f"[FAILED] - info is None")
                
        except Exception as e:
            print(f"[ERROR]: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_downloader())
