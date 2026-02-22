"""
Comprehensive test for all platform downloads
Tests: YouTube, Instagram, Facebook, TikTok
"""

import asyncio
import sys
import os

# Fix Unicode encoding issues on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))

from downloader import VideoDownloader


async def test_all_platforms():
    """Test video info extraction for all supported platforms"""
    
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    # Test URLs for each platform
    test_cases = [
        ("YouTube", "https://www.youtube.com/watch?v=jNQXAC9IVRw"),  # "Me at the zoo"
        ("Instagram", "https://www.instagram.com/p/C3sS8KLt-3W/"),  # Example public post
        ("TikTok", "https://www.tiktok.com/@scout2015/video/6718335390845095173"),  # Example
        # Facebook test removed - requires authentication usually
    ]
    
    results = {}
    
    for platform, url in test_cases:
        print(f"\n{'=' * 70}")
        print(f"Testing {platform}: {url}")
        print('=' * 70)
        
        try:
            # Test info extraction
            info = await downloader.get_video_info(url)
            
            if info:
                print(f"[INFO EXTRACTION: SUCCESS]")
                title = info.get('title', 'N/A')
                # Handle Unicode characters safely
                try:
                    title_display = title[:80] if title else 'N/A'
                except:
                    title_display = 'N/A'
                print(f"  Title: {title_display}")
                print(f"  Duration: {info.get('duration', 'N/A')} seconds")
                print(f"  Formats: {len(info.get('formats', []))} available")
                
                # Check for video formats
                video_formats = [f for f in info.get('formats', []) if f.get('vcodec') and f.get('vcodec') != 'none']
                if video_formats:
                    print(f"  Video formats: {len(video_formats)}")
                else:
                    print(f"  [WARNING] No video formats found")
                
                results[platform] = "SUCCESS"
            else:
                print(f"[INFO EXTRACTION: FAILED] - info is None")
                results[platform] = "FAILED - No info"
                
        except Exception as e:
            print(f"[ERROR]: {str(e)[:200]}")
            results[platform] = f"ERROR - {str(e)[:100]}"
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print('=' * 70)
    for platform, result in results.items():
        status_icon = "[OK]" if result == "SUCCESS" else "[FAIL]"
        print(f"{status_icon} {platform}: {result}")
    
    return results


if __name__ == "__main__":
    asyncio.run(test_all_platforms())
