# Vercel Deployment Guide - Video Downloader Frontend

## ⚠️ CRITICAL: Project Structure Configuration

Your project has `backend/` and `frontend/` in separate folders. Vercel needs to be configured to build from the `frontend/` directory.

## 🚀 Step-by-Step Deployment

### 1. Import Project to Vercel

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository

### 2. Configure Build Settings

**IMPORTANT**: In the project configuration screen:

#### Framework Preset
- Select: **Vite**

#### Root Directory
- Click **"Edit"** next to Root Directory
- Set to: `frontend`
- ✅ **This is critical!** Without this, Vercel will look for package.json in the root and fail.

#### Build & Development Settings
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### 3. Add Environment Variable

In the same configuration screen, expand **"Environment Variables"**:

- **Name**: `VITE_API_URL`
- **Value**: `https://video-downloader-production-e4fe.up.railway.app`
- **Environment**: Select all (Production, Preview, Development)

### 4. Deploy

Click **"Deploy"** button and wait for the build to complete.

---

## 🔧 If Already Deployed (Fixing Existing Deployment)

If you already have a Vercel project that's failing:

### Option A: Redeploy with Correct Settings

1. Go to your Vercel project dashboard
2. Click **Settings**
3. Scroll to **"Build & Development Settings"**

#### Set Root Directory:
- Click **"Edit"** next to Root Directory
- Enter: `frontend`
- Click **"Save"**

#### Verify Other Settings:
- Framework Preset: `Vite`
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

4. Go to **Settings** → **Environment Variables**
5. Add (if not exists):
   - Name: `VITE_API_URL`
   - Value: `https://video-downloader-production-e4fe.up.railway.app`
   - Environment: Production (check the box)
   - Click **"Save"**

6. Go to **Deployments** tab
7. Click the **three dots** on the latest deployment
8. Click **"Redeploy"**
9. Check **"Use existing Build Cache"** = OFF (unchecked)
10. Click **"Redeploy"**

---

## ✅ Verification

After successful deployment:

1. **Your Vercel URL**: https://video-downloader-jade.vercel.app/
2. **Backend Railway URL**: https://video-downloader-production-e4fe.up.railway.app/

### Test the deployment:
1. Open your Vercel URL in browser
2. You should see the Video Downloader homepage
3. Try analyzing a YouTube video URL
4. Check browser console (F12) for any CORS or API errors

---

## 🐛 Troubleshooting

### Error: "404: NOT_FOUND"
**Cause**: Vercel is looking for files in the wrong directory (root instead of `frontend/`)

**Fix**: 
1. Set Root Directory to `frontend` in project settings
2. Redeploy without cache

### Error: "Build failed - Cannot find package.json"
**Cause**: Root Directory not set correctly

**Fix**: 
1. Settings → General → Root Directory → `frontend`
2. Save and redeploy

### Error: "Network Error" or API calls failing in browser
**Cause**: Environment variable not set

**Fix**:
1. Settings → Environment Variables
2. Add `VITE_API_URL` = `https://video-downloader-production-e4fe.up.railway.app`
3. Redeploy

### CORS Errors in Browser Console
**Cause**: Backend doesn't recognize Vercel domain

**Fix**: Your backend is already configured to allow `*.vercel.app` domains automatically. If still getting CORS errors:
1. Check Railway backend is actually running
2. Verify Railway backend URL is correct
3. Add explicit environment variable on Railway:
   - Name: `FRONTEND_URL`
   - Value: `https://video-downloader-jade.vercel.app`

---

## 📝 Summary Checklist

Before deploying, ensure:

- ✅ Root Directory is set to `frontend`
- ✅ Framework Preset is `Vite`
- ✅ Environment variable `VITE_API_URL` is set to your Railway backend URL
- ✅ Railway backend is running and accessible
- ✅ Redeploy without cache if updating settings

---

## 🔗 URLs

- **Frontend (Vercel)**: https://video-downloader-jade.vercel.app/
- **Backend (Railway)**: https://video-downloader-production-e4fe.up.railway.app/
- **Backend Health Check**: https://video-downloader-production-e4fe.up.railway.app/health

---

## 🎯 Expected Result

After correct configuration:
1. Visiting your Vercel URL shows the Video Downloader interface
2. You can paste a video URL and click "Analyze"
3. Video information loads successfully
4. Download functionality works

If these work, your deployment is successful! 🎉
