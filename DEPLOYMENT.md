# Deployment Guide

This guide will help you deploy the Video Downloader application to production using Vercel (frontend) and Render.com (backend).

## Prerequisites

- GitHub account
- Vercel account (free tier available)
- Render.com account (free tier available)
- Git installed on your local machine

## Part 1: Push to GitHub

1. **Initialize Git Repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Video Downloader application"
   ```

2. **Create a new GitHub repository**:
   - Go to [GitHub](https://github.com)
   - Click "New repository"
   - Name it "video-downloader" (or any name you prefer)
   - Don't initialize with README (we already have code)
   - Click "Create repository"

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/video-downloader.git
   git branch -M main
   git push -u origin main
   ```

## Part 2: Deploy Backend to Render.com

### Step 1: Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub account if not already connected
4. Select your `video-downloader` repository
5. Configure the service:

   **Basic Settings:**
   - Name: `video-downloader-backend` (or any name)
   - Region: Choose closest to your users
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

   **Instance Type:**
   - Choose "Free" (or upgrade for better performance)

### Step 2: Add Environment Variables

In the "Environment" section, add:

- `PYTHON_VERSION`: `3.11.0`
- `FRONTEND_URL`: (leave blank for now, we'll update after frontend deployment)

### Step 3: Add Persistent Disk

1. Scroll to "Disks" section
2. Click "Add Disk"
3. Configure:
   - Name: `downloads`
   - Mount Path: `/opt/render/project/src/downloads`
   - Size: `1 GB` (or more if needed)

### Step 4: Create Service

1. Click "Create Web Service"
2. Wait for the deployment to complete (5-10 minutes)
3. Once deployed, copy your backend URL (e.g., `https://video-downloader-backend.onrender.com`)

**Important Note:** The free tier on Render spins down after 15 minutes of inactivity. The first request after inactivity may take 30-60 seconds to respond.

## Part 3: Deploy Frontend to Vercel

### Step 1: Import Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your `video-downloader` repository
4. Select the repository from the list

### Step 2: Configure Build Settings

Vercel should auto-detect the settings, but verify:

- **Framework Preset:** Vite
- **Root Directory:** `frontend`
- **Build Command:** `npm run build` (or leave as default)
- **Output Directory:** `dist` (or leave as default)

### Step 3: Add Environment Variables

In the "Environment Variables" section, add:

- **Key:** `VITE_API_URL`
- **Value:** Your Render backend URL (e.g., `https://video-downloader-backend.onrender.com`)
- **Environment:** All (Production, Preview, Development)

### Step 4: Deploy

1. Click "Deploy"
2. Wait for deployment to complete (2-3 minutes)
3. Once deployed, copy your frontend URL (e.g., `https://video-downloader.vercel.app`)

## Part 4: Update Backend CORS

### Step 1: Update Environment Variable

1. Go back to your Render.com dashboard
2. Select your backend service
3. Go to "Environment" tab
4. Update the `FRONTEND_URL` variable:
   - **Value:** Your Vercel URL (e.g., `https://video-downloader.vercel.app`)
5. Click "Save Changes"

### Step 2: Redeploy Backend

The backend will automatically redeploy with the new CORS settings.

## Part 5: Test Your Deployment

1. Visit your Vercel URL (e.g., `https://video-downloader.vercel.app`)
2. Try downloading a video from each platform:
   - YouTube
   - Facebook
   - Instagram
   - TikTok

**Note:** The first request to the backend may be slow if the free tier has spun down.

## Environment Variables Summary

### Frontend (.env)
```
VITE_API_URL=https://your-backend.onrender.com
```

### Backend (Render.com Environment Variables)
```
PYTHON_VERSION=3.11.0
FRONTEND_URL=https://your-frontend.vercel.app
```

## Troubleshooting

### Backend Issues

**Problem:** Backend not responding
- **Solution:** Free tier spins down after inactivity. Wait 30-60 seconds for it to wake up.

**Problem:** CORS errors in browser console
- **Solution:** Make sure `FRONTEND_URL` is set correctly in Render environment variables.

**Problem:** Download fails
- **Solution:** Check Render logs for FFmpeg errors. Ensure FFmpeg is available (it should be installed automatically).

### Frontend Issues

**Problem:** "Network Error" when analyzing video
- **Solution:** Check that `VITE_API_URL` is set correctly in Vercel environment variables.

**Problem:** Blank page after deployment
- **Solution:** Check Vercel deployment logs. Make sure build completed successfully.

### Performance Issues

**Problem:** Slow downloads on free tier
- **Solution:** Consider upgrading to a paid plan on Render for better performance.

**Problem:** Running out of disk space
- **Solution:** Increase the persistent disk size in Render (paid feature for >1GB).

## Updating Your Deployment

### Frontend Updates
1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update frontend"
   git push
   ```
2. Vercel will automatically deploy the new version

### Backend Updates
1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update backend"
   git push
   ```
2. Render will automatically deploy the new version

## Custom Domain (Optional)

### For Frontend (Vercel)
1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Update your DNS records as instructed

### For Backend (Render)
1. Go to your service settings in Render
2. Navigate to "Custom Domains"
3. Add your custom domain
4. Update your DNS records as instructed
5. Update `VITE_API_URL` in Vercel to use your custom backend domain

## Monitoring

### Backend Logs
- View logs in Render dashboard under your service → "Logs" tab
- Useful for debugging download issues and errors

### Frontend Analytics
- Vercel provides basic analytics automatically
- View in Vercel dashboard under your project → "Analytics"

## Security Considerations

1. **Rate Limiting:** Backend includes rate limiting (20 requests/minute per IP)
2. **CORS:** Only your frontend domain can access the API
3. **File Cleanup:** Downloaded files are automatically cleaned up after 1 hour
4. **HTTPS:** Both Vercel and Render provide free SSL certificates

## Cost Breakdown

### Free Tier Limits

**Vercel (Free):**
- 100 GB bandwidth/month
- Unlimited deployments
- Perfect for this project

**Render (Free):**
- 750 hours/month (enough for one service running 24/7)
- Spins down after 15 minutes of inactivity
- 1 GB persistent disk included
- May experience cold starts

### Paid Options

**Vercel Pro ($20/month):**
- Higher bandwidth limits
- Priority support
- Analytics

**Render Starter ($7/month):**
- No spin down
- Better performance
- More disk space options

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Render and Vercel logs
3. Check your environment variables
4. Verify your GitHub repository is up to date

---

## Quick Reference

### Important URLs
- Frontend: `https://your-project.vercel.app`
- Backend: `https://your-service.onrender.com`
- GitHub: `https://github.com/YOUR_USERNAME/video-downloader`

### Important Commands
```bash
# Local development
cd frontend && npm run dev        # Frontend (port 5173)
cd backend && uvicorn main:app --reload  # Backend (port 8000)

# Deploy updates
git add .
git commit -m "Your message"
git push  # Auto-deploys to both Vercel and Render
```

### Environment Variables
| Variable | Location | Example |
|----------|----------|---------|
| `VITE_API_URL` | Vercel | `https://your-backend.onrender.com` |
| `FRONTEND_URL` | Render | `https://your-frontend.vercel.app` |
| `PYTHON_VERSION` | Render | `3.11.0` |

---

**Congratulations!** 🎉 Your video downloader is now live and accessible to anyone with the URL.

Remember to comply with each platform's terms of service and only download content you have rights to download.
