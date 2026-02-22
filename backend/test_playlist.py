"""
Test playlist functionality
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from downloader import VideoDownloader


async def test_playlist():
    """Test playlist info extraction"""
    
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    # Test a small YouTube playlist
    test_url = "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
    
    print(f"Testing playlist: {test_url}")
    print('=' * 60)
    
    try:
        info = await downloader.get_playlist_info(test_url)
        
        if info:
            print(f"[SUCCESS!]")
            print(f"  Title: {info.get('title', 'N/A')}")
            print(f"  Uploader: {info.get('uploader', 'N/A')}")
            entries = info.get('entries', [])
            print(f"  Videos: {len(entries)}")
            
            if entries:
                print(f"\n  First 3 videos:")
                for i, entry in enumerate(entries[:3], 1):
                    if entry:
                        print(f"    {i}. {entry.get('title', 'N/A')}")
            else:
                print("  [WARNING] No entries found in playlist")
        else:
            print(f"[FAILED] - info is None")
            
    except Exception as e:
        print(f"[ERROR]: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_playlist())
