"""
Test Facebook video download functionality
"""

import asyncio
import sys
import os

# Fix Unicode encoding issues on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))

from downloader import VideoDownloader


async def test_facebook():
    """Test Facebook video download"""
    
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    # Test with a few different Facebook video URLs
    test_urls = [
        # Public Facebook video (example)
        "https://www.facebook.com/watch/?v=1234567890",  # Replace with actual public video
        # Feel free to add more test URLs
    ]
    
    print("=" * 70)
    print("Testing Facebook Video Download")
    print("=" * 70)
    
    for idx, url in enumerate(test_urls, 1):
        print(f"\nTest {idx}: {url}")
        print("-" * 70)
        
        try:
            # Test info extraction
            print("1. Getting video info...")
            info = await downloader.get_video_info(url)
            
            if info:
                print(f"   ✓ Info extraction successful")
                title = info.get('title', 'N/A')
                print(f"   Title: {title[:60] if title else 'N/A'}")
                print(f"   Duration: {info.get('duration', 'N/A')} seconds")
                print(f"   Formats: {len(info.get('formats', []))} available")
                
                # Test download
                print("\n2. Testing download...")
                result = await downloader.download_video(url, format_id='best')
                
                if result and 'filepath' in result:
                    filepath = result['filepath']
                    if os.path.exists(filepath):
                        filesize = os.path.getsize(filepath)
                        print(f"   ✓ Download successful!")
                        print(f"   File: {os.path.basename(filepath)}")
                        print(f"   Size: {filesize / 1024 / 1024:.2f} MB")
                        
                        # Clean up
                        try:
                            os.remove(filepath)
                            print(f"   ✓ Cleaned up test file")
                        except:
                            pass
                        
                        print(f"\n✓ Facebook download WORKING")
                        return True
                    else:
                        print(f"   ✗ File not found: {filepath}")
                else:
                    print(f"   ✗ Download failed")
            else:
                print(f"   ✗ Failed to get video info")
                
        except Exception as e:
            error_msg = str(e)
            print(f"   ✗ ERROR: {error_msg[:200]}")
            
            # Check for known issues
            if 'login' in error_msg.lower() or 'private' in error_msg.lower():
                print(f"   ℹ This video requires authentication")
                print(f"   ℹ Facebook restricts access to private/friends-only content")
            elif 'not found' in error_msg.lower() or '404' in error_msg:
                print(f"   ℹ Video not found or URL invalid")
            
            import traceback
            traceback.print_exc()
    
    print(f"\n✗ Facebook download testing inconclusive")
    print(f"ℹ Note: Facebook often requires authentication for most videos")
    print(f"ℹ Only public videos can be downloaded without login")
    return False


if __name__ == "__main__":
    result = asyncio.run(test_facebook())
    
    print("\n" + "=" * 70)
    print("FACEBOOK TEST RESULT")
    print("=" * 70)
    if result:
        print("✓ Facebook downloading is WORKING")
    else:
        print("⚠ Facebook requires authentication for most content")
        print("ℹ To test: Replace the URL in this file with a public Facebook video")
    print("=" * 70)
