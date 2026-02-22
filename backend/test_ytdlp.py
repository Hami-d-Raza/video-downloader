"""Quick test to check if yt-dlp is working"""
import yt_dlp

test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

try:
    ydl_opts = {
        'quiet': False,
        'skip_download': True,
        'no_warnings': False,
    }
    
    print(f"Testing yt-dlp with URL: {test_url}")
    print("=" * 50)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(test_url, download=False)
        
        if info:
            print(f"\n✓ Success!")
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Duration: {info.get('duration', 'N/A')}")
            print(f"Uploader: {info.get('uploader', 'N/A')}")
        else:
            print("\n✗ Failed - info is None")
            
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
