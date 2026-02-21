# Deploy Backend to Railway

## ✅ Configuration Complete
All conflicting deployment files have been removed. Your backend is now ready for Railway.

## 📋 Deployment Steps

### 1. Create Railway Project
1. Go to [Railway](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `video-downloader` repository

### 2. Configure Root Directory
⚠️ **CRITICAL STEP** - Railway MUST know the backend is in a subdirectory:

1. In Railway dashboard, go to your service
2. Click **Settings** tab
3. Find **"Root Directory"** setting
4. Set it to: `backend`
5. Click **Save**

### 3. Configure Build
Railway will automatically detect:
- `nixpacks.toml` - Build configuration (Python 3.9 + FFmpeg)
- `railway.json` - Deployment settings
- `requirements.txt` - Python dependencies

No manual configuration needed!

### 4. Environment Variables (Optional)
Add these if needed:
- `FRONTEND_URL` = Your Vercel URL (e.g., `https://your-app.vercel.app`)

### 5. Deploy
1. Railway will automatically start building
2. Wait for build to complete (2-3 minutes)
3. Railway will provide a URL like: `https://your-backend.up.railway.app`

## 🔗 Connect Frontend to Backend

Once deployed, copy your Railway URL and update Vercel:

1. Go to Vercel dashboard → Your project → Settings → Environment Variables
2. Add/Update:
   - `VITE_API_URL` = `https://your-backend.up.railway.app`
3. Redeploy frontend

## ✨ What Was Cleaned Up
Removed conflicting files:
- ❌ `.python-version` (conflicted with nixpacks.toml)
- ❌ `render.yaml` (wrong platform)
- ❌ `Dockerfile` (Railway uses Nixpacks, not Docker)
- ❌ `start.sh` (redundant with nixpacks.toml)

Kept only:
- ✅ `nixpacks.toml` - Primary build config
- ✅ `railway.json` - Deployment settings
- ✅ `Procfile` - Backup start command
- ✅ `runtime.txt` - Python version
- ✅ `requirements.txt` - Dependencies

## 🐛 Troubleshooting

### Build still failing?
1. Verify "Root Directory" is set to `backend`
2. Check Railway build logs for specific errors
3. Ensure all changes are pushed to GitHub

### CORS errors after deployment?
The backend already allows:
- `*.vercel.app`
- `*.netlify.app`
- `*.up.railway.app`

Just update `VITE_API_URL` in Vercel and redeploy.

## 📝 Changes Committed
Latest commits:
- `3179887` - Remove conflicting deployment files
- `e49a9d6` - Simplify Railway configuration
- All changes pushed to GitHub

Your repository is ready for Railway deployment!
