"""Quick summary test"""
import asyncio
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
from downloader import VideoDownloader

async def quick_test():
    downloader = VideoDownloader("downloads")
    
    tests = [
        ("YouTube", "https://www.youtube.com/watch?v=jNQXAC9IVRw"),
        ("Instagram", "https://www.instagram.com/p/C3sS8KLt-3W/"),
        ("TikTok", "https://www.tiktok.com/@scout2015/video/6718335390845095173"),
    ]
    
    print("\nPLATFORM TEST RESULTS")
    print("=" * 50)
    
    for platform, url in tests:
        try:
            info = await downloader.get_video_info(url)
            if info:
                print(f"[OK] {platform}: SUCCESS - {info.get('title', 'N/A')[:40]}")
            else:
                print(f"[FAIL] {platform}: No info returned")
        except Exception as e:
            error = str(e)[:60]
            print(f"[FAIL] {platform}: {error}")
    
    print("=" * 50)

asyncio.run(quick_test())
