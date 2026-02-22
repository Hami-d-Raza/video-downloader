# Production Deployment Guide - Vercel + Railway

**Complete step-by-step guide to deploy Video Downloader to production**

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ GitHub account
- ✅ Vercel account (sign up at [vercel.com](https://vercel.com))
- ✅ Railway account (already set up with backend)
- ✅ Project pushed to GitHub
- ✅ Backend URL from Railway: `https://video-downloader-production-e4fe.up.railway.app`

---

## 🏗️ Project Structure Overview

This is a **monorepo** with two separate applications:

```
video-downloader/
├── backend/          # FastAPI backend (deployed to Railway)
│   ├── main.py
│   ├── downloader.py
│   ├── requirements.txt
│   └── ...
└── frontend/         # React frontend (deploy to Vercel)
    ├── src/
    ├── public/
    ├── package.json
    ├── vercel.json
    └── ...
```

**Critical**: Vercel must be configured to build from the `frontend/` directory!

---

## 🚀 Part 1: Deploy Frontend to Vercel

### Step 1: Create New Project

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Click **"Import Git Repository"**
4. Select your `video-downloader` repository
5. Click **"Import"**

### Step 2: Configure Build Settings

**⚠️ CRITICAL**: This step is essential for success!

In the "Configure Project" screen:

#### A. Framework Preset
- Select: **Vite**

#### B. Root Directory
This is the most important setting!

1. Find **"Root Directory"** section
2. Click **"Edit"** button
3. Enter: `frontend`
4. Click **"Continue"**

#### C. Build & Development Settings

These should auto-populate, but verify:

- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

If they don't auto-populate, enter them manually.

### Step 3: Add Environment Variables

Still in the "Configure Project" screen:

1. Scroll to **"Environment Variables"** section
2. Click to expand it
3. Add the following variable:

| Name | Value | Environment |
|------|-------|-------------|
| `VITE_API_URL` | `https://video-downloader-production-e4fe.up.railway.app` | Production ✓ |

**Note**: Replace the URL with your actual Railway backend URL if different.

### Step 4: Deploy!

1. Click the **"Deploy"** button
2. Wait 2-3 minutes for the build to complete
3. You'll see a success screen with your deployment URL

**Your frontend URL will be**: `https://video-downloader-jade.vercel.app`

(Or similar with a different subdomain)

---

## 🔗 Part 2: Update Backend CORS

Now that you have your Vercel URL, update the backend:

### Step 1: Verify Backend is Working

1. **Check backend health**:
   - Visit: `https://video-downloader-production-e4fe.up.railway.app/health`
   - Should return JSON with `ffmpeg_installed: true`
   - If FFmpeg shows as `false`, the backend needs to redeploy with latest code

2. **If FFmpeg is not installed**:
   - Pull latest code: `git pull origin main`
   - Railway will auto-redeploy with FFmpeg
   - Check `/health` again after ~2 minutes

### Step 2: Add Frontend URL to Railway

1. Go to [railway.app/dashboard](https://railway.app/dashboard)
2. Open your backend service
3. Click on **"Variables"** tab
4. Click **"+ New Variable"**
5. Add:
   - **Variable**: `FRONTEND_URL`
   - **Value**: `https://video-downloader-jade.vercel.app`
6. Click **"Add"**

The backend will automatically redeploy with new CORS settings.

---

## ✅ Part 3: Verify Deployment

### Test Your Application

1. Visit your Vercel URL: `https://video-downloader-jade.vercel.app`
2. You should see the Video Downloader homepage
3. Test with a YouTube video:
   - Paste: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Click "Analyze Video"
   - Video information should load
4. Try downloading (select a format and click download)

### Check Browser Console

Press `F12` to open Developer Tools:

- ✅ No CORS errors
- ✅ No 404 errors
- ✅ API calls succeed
- ✅ You see: `🔗 API Base URL: https://video-downloader-production-e4fe.up.railway.app` (only in dev mode)

---

## 🐛 Troubleshooting Common Issues

### Issue 1: 404 NOT_FOUND Error

**Symptom**: Blank page or "404: NOT_FOUND" error

**Cause**: Root Directory not set to `frontend`

**Fix**:
1. Go to Vercel Project → **Settings** → **General**
2. Find **"Root Directory"**
3. Click **"Edit"**
4. Set to: `frontend`
5. Click **"Save"**
6. Go to **Deployments** tab
7. Click **⋯** (three dots) on latest deployment
8. Click **"Redeploy"**
9. **Uncheck** "Use existing Build Cache"
10. Click **"Redeploy"**

### Issue 2: Build Fails - "Cannot find package.json"

**Symptom**: Build fails with error about missing package.json

**Cause**: Root Directory not configured correctly

**Fix**: Same as Issue 1 above

### Issue 3: ESLint Dependency Conflict

**Symptom**: Build fails with error like:
```
Could not resolve dependency:
peer eslint@"^3 || ^4 || ^5 || ^6 || ^7 || ^8 || ^9.7" from eslint-plugin-react
```

**Cause**: ESLint version incompatibility with plugins

**Fix**: This has already been fixed in the latest commit. If you still see this:

1. Pull the latest code: `git pull origin main`
2. Clear Vercel build cache and redeploy
3. The package.json now uses ESLint 8.57 (stable and compatible)

**Note**: This issue is automatically resolved in the current version.

### Issue 4: White Screen / Blank Page

**Symptom**: Deployment succeeds but shows blank page

**Possible Causes & Fixes**:

1. **Check browser console** (F12) for errors
2. **Verify environment variable**:
   - Settings → Environment Variables
   - Ensure `VITE_API_URL` is set
3. **Clear cache and redeploy**:
   - Deployments → ⋯ → Redeploy
   - Uncheck "Use existing Build Cache"

### Issue 5: "Network Error" When Analyzing Videos

**Symptom**: Can see the page, but analyzing videos fails

**Cause**: API URL not configured or backend not responding

**Fix**:

1. **Verify backend is running**:
   - Visit: `https://video-downloader-production-e4fe.up.railway.app/health`
   - Should return: `{"status":"healthy"}`

2. **Check environment variable**:
   - Vercel → Settings → Environment Variables
   - Ensure `VITE_API_URL` is correct
   - Redeploy after adding/changing

3. **Check browser console**:
   - Look for CORS errors
   - Verify API URL is correct

### Issue 6: CORS Errors in Browser

**Symptom**: Errors like "blocked by CORS policy" in console

**Cause**: Backend doesn't recognize frontend domain

**Fix**:

1. **Add FRONTEND_URL to Railway**:
   - Railway → Backend Service → Variables
   - Add: `FRONTEND_URL` = `https://your-vercel-url.vercel.app`
   
2. **Verify backend CORS config**:
   - Backend already supports `*.vercel.app` domains
   - Should work automatically

### Issue 7: 500 Error When Downloading Videos

**Symptom**: Analyze works, but download fails with 500 error

**Cause**: FFmpeg not installed on Railway (required for video processing)

**Fix**: This has been fixed in the latest code. To apply:

1. **Pull latest code**:
   ```bash
   git pull origin main
   ```

2. **Railway auto-redeploys** with FFmpeg configured via `nixpacks.toml`

3. **Verify FFmpeg is installed**:
   - Visit: `https://video-downloader-production-e4fe.up.railway.app/health`
   - Check: `"ffmpeg_installed": true`

4. **If still false after 2 minutes**:
   - Go to Railway → Backend Service → Settings
   - Click "Redeploy" to force rebuild

**What was fixed**:
- Added `backend/nixpacks.toml` to install FFmpeg via Nix packages
- Updated health check endpoint to verify FFmpeg installation
- FFmpeg is required for merging video+audio, format conversion, and MP3 extraction

### Issue 8: YouTube 403 Forbidden Error

**Symptom**: Analysis works, but download fails with "HTTP Error 403: Forbidden"

**Cause**: Outdated yt-dlp version - YouTube blocks old versions

**Fix**: This has been fixed in the latest code (yt-dlp always updates to latest):

1. **Pull latest code**:
   ```bash
   git pull origin main
   ```

2. **Railway auto-redeploys** with latest yt-dlp

3. **Test download** - should work now!

**What was fixed**:
- Removed yt-dlp version pin (was stuck at 2023.10.7)
- Now installs latest yt-dlp on every deployment
- Updated Python from 3.9 → 3.11 (yt-dlp requirement)
- YouTube frequently changes their API, so latest yt-dlp is essential

**Prevention**: The latest code always installs the newest yt-dlp version automatically.

---

## 🔄 Updating Your Deployment

### Frontend Updates

When you make changes to the frontend:

```bash
# 1. Commit and push to GitHub
git add .
git commit -m "Update frontend"
git push origin main

# 2. Vercel will automatically deploy the new version!
```

Vercel deploys automatically on every push to main branch.

### Manual Redeploy

If you need to manually trigger a redeployment:

1. Go to Vercel Dashboard → Your Project
2. Click **Deployments** tab
3. Click **⋯** on the deployment you want to redeploy
4. Click **"Redeploy"**

---

## 🎯 Environment Variables Reference

### Vercel (Frontend)

| Variable | Value | Purpose |
|----------|-------|---------|
| `VITE_API_URL` | `https://video-downloader-production-e4fe.up.railway.app` | Backend API endpoint |

### Railway (Backend)

| Variable | Value | Purpose |
|----------|-------|---------|
| `FRONTEND_URL` | `https://video-downloader-jade.vercel.app` | Frontend URL for CORS |
| `PYTHON_VERSION` | `3.11` | Python version (optional) |

---

## 📊 Production Deployment URLs

Track your deployment URLs here:

- **Frontend (Vercel)**: `https://video-downloader-jade.vercel.app`
- **Backend (Railway)**: `https://video-downloader-production-e4fe.up.railway.app`
- **Backend Health Check**: `https://video-downloader-production-e4fe.up.railway.app/health`

---

## 🔐 Security Best Practices

✅ **Already implemented**:
- Environment variables for sensitive config
- CORS protection
- Rate limiting on backend
- Input validation
- Secure headers

⚠️ **Never commit**:
- `.env` files
- API keys
- Sensitive credentials

---

## 🎓 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [Railway Documentation](https://docs.railway.app)

---

## ✨ Post-Deployment Checklist

After successful deployment, verify:

- [ ] Frontend loads at Vercel URL
- [ ] Can analyze YouTube videos
- [ ] Can analyze Facebook videos  
- [ ] Can analyze Instagram videos
- [ ] Can analyze TikTok videos
- [ ] Can download videos successfully
- [ ] Audio-only download works
- [ ] Playlist analysis works
- [ ] Mobile responsive design works
- [ ] No console errors in browser
- [ ] Backend health check responds
- [ ] CORS working properly

---

## 🎉 Success!

If all checks pass, your Video Downloader is now live in production!

Share your URL: `https://video-downloader-jade.vercel.app`

---

## 📞 Quick Help

**Deployment still failing?**

1. Double-check Root Directory is set to `frontend`
2. Verify `VITE_API_URL` environment variable is set
3. Ensure backend Railway service is running
4. Check Vercel build logs for specific errors
5. Clear build cache and redeploy

**Common error patterns**:
- `404 NOT_FOUND` → Root Directory wrong
- `Cannot find package.json` → Root Directory wrong
- `Network Error` → Environment variable or backend issue
- `CORS error` → Backend FRONTEND_URL not set

---

Made with ❤️ using React, FastAPI, Vite, and Vercel
