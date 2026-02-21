# Railway Deployment Guide for Video Downloader

This guide will help you deploy both the backend and frontend of the Video Downloader application on Railway.

## Prerequisites

1. A Railway account (sign up at https://railway.app)
2. Git repository pushed to GitHub/GitLab/Bitbucket
3. Your code committed and pushed

## Deployment Steps

### Option 1: Deploy Both Services (Recommended)

#### Step 1: Deploy Backend

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `Video Downloader` repository
5. Railway will detect the project - click **"Add variables"**
6. Set the **Root Directory** to `backend`
7. Add environment variables (optional):
   - `FRONTEND_URL` = (will be filled after frontend deployment)
8. Click **"Deploy"**
9. Wait for deployment to complete
10. **Copy the backend URL** (e.g., `https://your-backend.up.railway.app`)

#### Step 2: Deploy Frontend

1. In the same Railway project, click **"New Service"**
2. Select **"GitHub Repo"** (same repository)
3. Set the **Root Directory** to `frontend`
4. Add environment variable:
   - Key: `VITE_API_URL`
   - Value: `https://your-backend.up.railway.app` (from Step 1)
5. Click **"Deploy"**
6. Wait for deployment to complete
7. **Copy the frontend URL** (e.g., `https://your-frontend.up.railway.app`)

#### Step 3: Update Backend CORS

1. Go back to the **Backend service**
2. Add/update environment variable:
   - Key: `FRONTEND_URL`
   - Value: `https://your-frontend.up.railway.app`
3. The backend will automatically redeploy

### Option 2: Quick Deploy (Simplified)

If you want to deploy just the backend for testing:

1. Create a new Railway project
2. Deploy from GitHub
3. Set root directory to `backend`
4. Deploy
5. Use the provided URL to test API endpoints

## Environment Variables Reference

### Backend Service
- `PORT` - Automatically set by Railway
- `FRONTEND_URL` - Your frontend URL (for CORS)
- `DOWNLOAD_DIR` - (Optional) Custom download directory

### Frontend Service
- `PORT` - Automatically set by Railway
- `VITE_API_URL` - Your backend API URL

## Important Notes

### File Storage
⚠️ **Railway uses ephemeral storage** - downloaded files are temporary and will be deleted when the service restarts. For production use, consider:
- Integrating with cloud storage (AWS S3, Cloudflare R2, etc.)
- Streaming downloads directly to users without server storage

### FFmpeg
The backend includes FFmpeg in the nixpacks.toml configuration for video processing.

### Build Configuration

Both services include:
- `railway.json` - Railway-specific configuration
- `nixpacks.toml` - Build configuration (backend only)
- `Procfile` - Process configuration (backend only)

## Troubleshooting

### "There was an error deploying from source"

**Cause**: Railway couldn't detect how to build your project

**Solutions**:
1. Make sure you set the correct **Root Directory** (`backend` or `frontend`)
2. Check that `railway.json` exists in the service directory
3. Verify `requirements.txt` (backend) or `package.json` (frontend) is present

### Build fails for Backend

**Check**:
- Python version compatibility (using Python 3.9)
- All dependencies in `requirements.txt` are valid
- View build logs in Railway dashboard

### Build fails for Frontend

**Check**:
- Node version (Railway uses Node 18+ by default)
- All dependencies in `package.json` are valid
- Build command completes successfully locally

### CORS Errors

**Fix**:
1. Make sure `FRONTEND_URL` is set in backend environment variables
2. Include your frontend Railway URL in the CORS configuration
3. Redeploy backend after updating environment variables

### 404 on Frontend Routes

**Fix**:
Update `frontend/vite.config.js` to include:
```javascript
build: {
  outDir: 'dist'
},
preview: {
  port: 4173,
  strictPort: false,
  host: '0.0.0.0'
}
```

## Monitoring

- View logs in Railway dashboard
- Monitor service health and restarts
- Check resource usage (RAM, CPU)

## Cost Considerations

Railway offers:
- **Free tier**: $5 worth of usage per month
- **Pro plan**: $20/month with $20 credits

For this application:
- Backend: ~$5-10/month (depending on usage)
- Frontend: ~$3-5/month
- Total: ~$8-15/month (may fit in free tier for low usage)

## Need Help?

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Create an issue in your repository
