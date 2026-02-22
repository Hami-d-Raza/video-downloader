"""
Test Instagram download functionality
Run this to verify Instagram downloads are working
"""

import asyncio
import sys
import os

# Add parent directory to path to import downloader
sys.path.insert(0, os.path.dirname(__file__))

from downloader import VideoDownloader


async def test_instagram():
    """Test Instagram video info extraction and quality selection"""
    
    print("Testing Instagram functionality...")
    print("=" * 50)
    
    # Initialize downloader
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    downloader = VideoDownloader(download_dir)
    
    # Test URL - you can replace this with any public Instagram video URL
    # For now, we'll just test if the extractor is properly configured
    test_url = input("Enter an Instagram video URL to test (or press Enter to skip): ").strip()
    
    if not test_url:
        print("\nNo URL provided. Skipping download test.")
        print("To test, run this script again and provide an Instagram video URL.")
        return
    
    if 'instagram.com' not in test_url.lower():
        print("Error: Please provide a valid Instagram URL")
        return
    
    try:
        print(f"\nAttempting to get info for: {test_url}")
        info = await downloader.get_video_info(test_url)
        
        if info:
            print("\n✓ Successfully retrieved Instagram video info!")
            print(f"  Title: {info.get('title', 'N/A')}")
            print(f"  Duration: {info.get('duration', 'N/A')} seconds")
            print(f"  Uploader: {info.get('uploader', 'N/A')}")
            
            # Check thumbnail
            thumbnail = info.get('thumbnail') or info.get('display_url')
            if thumbnail:
                print(f"  Thumbnail: ✓ Found ({thumbnail[:60]}...)")
            else:
                print(f"  Thumbnail: ✗ Not found")
                # Show available thumbnail fields for debugging
                thumb_fields = {k: v for k, v in info.items() if 'thumb' in k.lower() or 'image' in k.lower() or 'display' in k.lower()}
                if thumb_fields:
                    print(f"  Available image fields: {list(thumb_fields.keys())}")
            
            # Check available formats
            formats = info.get('formats', [])
            print(f"\n  Total formats available: {len(formats)}")
            
            # Extract and display available video heights
            video_heights = set()
            for fmt in formats:
                if fmt.get('vcodec') and fmt.get('vcodec') != 'none':
                    height = fmt.get('height')
                    if height:
                        video_heights.add(height)
            
            if video_heights:
                print(f"  Available video heights: {sorted(video_heights, reverse=True)}")
                print("\n✓ Quality selection should work for this video!")
            else:
                print("  No video heights found (might be a photo post)")
            
            print("\nInstagram download capability is working! ✓")
            
            # Test quality selection
            test_download = input("\nDo you want to test downloading? (y/n): ").strip().lower()
            if test_download == 'y':
                quality = input("Enter quality (e.g., 720p, 480p, or 'best'): ").strip()
                
                if quality and quality != 'best':
                    print(f"\nDownloading in {quality} quality...")
                    result = await downloader.download_video(test_url, format_id=quality)
                else:
                    print("\nDownloading in best quality...")
                    result = await downloader.download_video(test_url)
                
                if result and result.get('filepath'):
                    print(f"✓ Download successful!")
                    print(f"  File: {result['filepath']}")
                    print(f"  Size: {result.get('filesize', 0) / (1024*1024):.2f} MB")
                else:
                    print("✗ Download failed")
        else:
            print("\n✗ Failed to retrieve video info")
            print("This might be due to:")
            print("  - Private account/video")
            print("  - Invalid URL")
            print("  - Network issues")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nIf you're seeing authentication errors, Instagram may require:")
        print("  1. Login cookies")
        print("  2. The video must be from a public account")


if __name__ == "__main__":
    asyncio.run(test_instagram())
