"""
Quick test to verify YouTube download actually works
"""

import asyncio
import sys
import os

# Fix Unicode encoding issues on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))

from downloader import VideoDownloader


async def test_youtube_download():
    """Test YouTube video download"""
    
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    # Test YouTube download
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video ever
    
    print(f"Testing YouTube download: {url}")
    print("=" * 70)
    
    try:
        # Get info first
        print("1. Getting video info...")
        info = await downloader.get_video_info(url)
        
        if info:
            print(f"   ✓ Title: {info.get('title', 'N/A')}")
            print(f"   ✓ Duration: {info.get('duration', 'N/A')} seconds")
            print(f"   ✓ Formats available: {len(info.get('formats', []))}")
        else:
            print("   ✗ Failed to get video info")
            return False
        
        # Now download
        print("\n2. Downloading video...")
        result = await downloader.download_video(url, format_id='best', audio_only=False)
        
        if result and 'filepath' in result:
            filepath = result['filepath']
            if os.path.exists(filepath):
                filesize = os.path.getsize(filepath)
                print(f"   ✓ Download successful!")
                print(f"   ✓ File: {os.path.basename(filepath)}")
                print(f"   ✓ Size: {filesize / 1024 / 1024:.2f} MB")
                
                # Clean up test file
                try:
                    os.remove(filepath)
                    print(f"   ✓ Cleaned up test file")
                except:
                    pass
                
                return True
            else:
                print(f"   ✗ File not found: {filepath}")
                return False
        else:
            print("   ✗ Download failed - no result")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False


async def test_tiktok_download():
    """Test TikTok video download"""
    
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    # Test TikTok download
    url = "https://www.tiktok.com/@scout2015/video/6718335390845095173"
    
    print(f"\nTesting TikTok download: {url}")
    print("=" * 70)
    
    try:
        # Get info first
        print("1. Getting video info...")
        info = await downloader.get_video_info(url)
        
        if info:
            print(f"   ✓ Title: {info.get('title', 'N/A')[:80]}")
            print(f"   ✓ Duration: {info.get('duration', 'N/A')} seconds")
        else:
            print("   ✗ Failed to get video info")
            return False
        
        # Now download
        print("\n2. Downloading video...")
        result = await downloader.download_video(url, format_id='best', audio_only=False)
        
        if result and 'filepath' in result:
            filepath = result['filepath']
            if os.path.exists(filepath):
                filesize = os.path.getsize(filepath)
                print(f"   ✓ Download successful!")
                print(f"   ✓ File: {os.path.basename(filepath)}")
                print(f"   ✓ Size: {filesize / 1024 / 1024:.2f} MB")
                
                # Clean up test file
                try:
                    os.remove(filepath)
                    print(f"   ✓ Cleaned up test file")
                except:
                    pass
                
                return True
            else:
                print(f"   ✗ File not found: {filepath}")
                return False
        else:
            print("   ✗ Download failed - no result")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all download tests"""
    
    results = {}
    
    # Test YouTube
    results['YouTube'] = await test_youtube_download()
    
    # Test TikTok
    results['TikTok'] = await test_tiktok_download()
    
    # Summary
    print("\n" + "=" * 70)
    print("DOWNLOAD TEST SUMMARY")
    print("=" * 70)
    
    for platform, success in results.items():
        status = "[✓ PASS]" if success else "[✗ FAIL]"
        print(f"{status} {platform}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed")
    
    return all_passed


if __name__ == "__main__":
    asyncio.run(main())
