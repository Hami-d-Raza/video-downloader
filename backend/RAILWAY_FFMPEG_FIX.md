# Railway Backend Deployment - FFmpeg Fix

## Issue

Downloads were failing with 500 error because FFmpeg was not properly installed on Railway.

## Solution

Added `nixpacks.toml` configuration to ensure FFmpeg is installed as a Nix package (not apt package).

## Files Modified

1. **backend/nixpacks.toml** - Created to specify FFmpeg as Nix package
2. **backend/railway.json** - Simplified to use nixpacks.toml configuration

## How to Apply

1. Commit and push changes:
```bash
git add backend/nixpacks.toml backend/railway.json
git commit -m "Fix Railway FFmpeg installation for video downloads"
git push
```

2. Railway will automatically:
   - Detect nixpacks.toml
   - Install FFmpeg via Nix packages
   - Redeploy the backend
   - Video downloads will now work

## Verification

After deployment completes:
1. Visit your frontend: https://video-downloader-jade.vercel.app
2. Try downloading a YouTube video
3. Download should now succeed (no more 500 error)

## Why This Fix Works

- Railway uses Nixpacks for builds
- Nix packages (`nixPkgs`) are the correct way to install system dependencies
- `aptPkgs` in railway.json wasn't working properly
- FFmpeg is required for:
  - Merging video + audio streams
  - Converting to MP4/MP3
  - Post-processing downloaded content
