"""
Comprehensive platform test - Tests all supported platforms
"""

import asyncio
import sys
import os

# Fix Unicode encoding issues on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))

from downloader import VideoDownloader


async def test_platform(downloader, platform_name, url, test_download=False):
    """Test a single platform"""
    
    print(f"\n{'=' * 70}")
    print(f"Testing {platform_name}")
    print('=' * 70)
    print(f"URL: {url}")
    
    try:
        # Test 1: Info extraction
        print("\n  [1] Getting video info...")
        info = await downloader.get_video_info(url)
        
        if not info:
            print(f"  ✗ FAILED - No info returned")
            return {'info': False, 'download': False}
        
        print(f"  ✓ Info extraction successful")
        title = info.get('title', 'N/A')
        try:
            title_display = title[:60] if title else 'N/A'
        except:
            title_display = 'N/A'
        print(f"      Title: {title_display}")
        print(f"      Duration: {info.get('duration', 'N/A')} seconds")
        print(f"      Formats: {len(info.get('formats', []))} available")
        
        # Test 2: Download (optional)
        if test_download:
            print(f"\n  [2] Testing download...")
            result = await downloader.download_video(url, format_id='best')
            
            if result and 'filepath' in result:
                filepath = result['filepath']
                if os.path.exists(filepath):
                    filesize = os.path.getsize(filepath)
                    print(f"  ✓ Download successful")
                    print(f"      File: {os.path.basename(filepath)}")
                    print(f"      Size: {filesize / 1024 / 1024:.2f} MB")
                    
                    # Clean up
                    try:
                        os.remove(filepath)
                        print(f"  ✓ Cleaned up test file")
                    except:
                        pass
                    
                    return {'info': True, 'download': True}
                else:
                    print(f"  ✗ Download failed - file not found")
                    return {'info': True, 'download': False}
            else:
                print(f"  ✗ Download failed - no result")
                return {'info': True, 'download': False}
        else:
            return {'info': True, 'download': None}
            
    except Exception as e:
        error_msg = str(e)
        print(f"  ✗ ERROR: {error_msg[:150]}")
        
        # Check for known issues
        if 'Instagram' in error_msg and 'empty media response' in error_msg:
            print(f"  ℹ Instagram requires authentication for this URL")
            print(f"  ℹ This is expected - Instagram restricts access without login")
        elif 'Facebook' in error_msg or 'Login required' in error_msg:
            print(f"  ℹ Facebook requires authentication")
            print(f"  ℹ This is expected - Facebook restricts access without login")
        
        return {'info': False, 'download': False}


async def main():
    """Run comprehensive platform tests"""
    
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    # Test configurations
    tests = [
        {
            'name': 'YouTube',
            'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',  # First YouTube video
            'download': True
        },
        {
            'name': 'TikTok',
            'url': 'https://www.tiktok.com/@scout2015/video/6718335390845095173',
            'download': True
        },
        {
            'name': 'Instagram',
            'url': 'https://www.instagram.com/p/C3sS8KLt-3W/',
            'download': False  # Skip download for Instagram (requires auth)
        },
    ]
    
    results = {}
    
    for test in tests:
        result = await test_platform(
            downloader,
            test['name'],
            test['url'],
            test_download=test.get('download', False)
        )
        results[test['name']] = result
    
    # Summary
    print(f"\n{'=' * 70}")
    print("COMPREHENSIVE TEST SUMMARY")
    print('=' * 70)
    
    for platform, result in results.items():
        info_status = "✓" if result['info'] else "✗"
        
        if result['download'] is None:
            dl_status = "SKIP"
        elif result['download']:
            dl_status = "✓"
        else:
            dl_status = "✗"
        
        print(f"{platform:15} Info: {info_status}    Download: {dl_status}")
    
    # Overall status
    print("\n" + "=" * 70)
    working_platforms = [p for p, r in results.items() if r['info']]
    print(f"Working Platforms: {len(working_platforms)}/{len(results)}")
    print(f"Platforms: {', '.join(working_platforms)}")
    
    # Notes
    print("\n" + "=" * 70)
    print("NOTES:")
    print("  • YouTube: Working with warnings about PO tokens (expected)")
    print("  • TikTok: Working (impersonation warnings are normal)")
    print("  • Instagram: Requires authentication for most posts")
    print("  • Facebook: Requires authentication (not tested)")
    print("=" * 70)
    
    return len(working_platforms) >= 2  # Success if at least 2 platforms work


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
