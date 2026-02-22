"""
Test batch download with playlist URLs
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from downloader import VideoDownloader


async def test_batch_download():
    """Test batch download with a small playlist"""
    
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    # Test with 2 videos from playlist
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley
        "https://www.youtube.com/watch?v=L_jWHffIx5E",  # Smash Mouth
    ]
    
    print(f"Testing batch download with {len(test_urls)} videos")
    print('=' * 60)
    
    try:
        result = await downloader.download_batch(
            urls=test_urls,
            format_id="360p",  # Use low quality for faster test
            audio_only=False
        )
        
        if result:
            print(f"[SUCCESS!]")
            print(f"  ZIP File: {result.get('filename', 'N/A')}")
            print(f"  Total: {result.get('total', 0)}")
            print(f"  Successful: {result.get('successful', 0)}")
            print(f"  Failed: {result.get('failed', 0)}")
            
            # Check if ZIP exists
            filepath = result.get('filepath')
            if filepath and os.path.exists(filepath):
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  ZIP Size: {size_mb:.2f} MB")
            else:
                print(f"  [WARNING] ZIP file not found at: {filepath}")
        else:
            print(f"[FAILED] - result is None")
            
    except Exception as e:
        print(f"[ERROR]: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("NOTE: This will actually download 2 videos. It may take 1-2 minutes.")
    print("Press Ctrl+C to cancel within 5 seconds...")
    import time
    time.sleep(5)
    asyncio.run(test_batch_download())
