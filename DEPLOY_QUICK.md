# Quick Railway Deployment Steps

## Deploying to Railway (Fast Track)

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Deploy Backend
1. Go to https://railway.app → **New Project**
2. Choose **"Deploy from GitHub repo"**
3. Select your repository
4. **Important**: Set **Root Directory** to `backend`
5. Railway will auto-detect and deploy
6. **Copy the backend URL** (e.g., `https://video-downloader-backend-production.up.railway.app`)

### 3. Deploy Frontend
1. In the same project, click **"New Service"**
2. Select the same GitHub repository
3. **Important**: Set **Root Directory** to `frontend`
4. Add environment variable:
   - `VITE_API_URL` = (paste your backend URL from step 2)
5. Deploy
6. **Copy the frontend URL**

### 4. Update Backend CORS
1. Go to backend service → Variables
2. Add: `FRONTEND_URL` = (paste your frontend URL from step 3)
3. Backend will auto-redeploy

### Done! 🎉
Your app is now live on Railway.

## Common Issues & Fixes

### ❌ "There was an error deploying from source" or "Script start.sh not found"
**Fix**: Make sure you set the **Root Directory** correctly:
- Backend service: `backend`
- Frontend service: `frontend`

Also ensure you've pushed all the configuration files:
```bash
git add .
git commit -m "Add Railway config files"
git push origin main
```

### ❌ Build fails with "No package.json" or "No requirements.txt"  
**Fix**: Verify the Root Directory is set correctly in service settings

### ❌ Frontend shows "Network Error" when testing
**Fix**: Make sure:
1. `VITE_API_URL` is set in frontend service
2. `FRONTEND_URL` is set in backend service
3. Both URLs should start with `https://`

### ❌ CORS errors in browser console
**Fix**: 
1. Check `FRONTEND_URL` is set correctly in backend
2. Redeploy backend after adding environment variable
3. Make sure URLs don't have trailing slashes

## Environment Variables Quick Reference

### Backend Service
```
FRONTEND_URL=https://your-frontend.up.railway.app
```

### Frontend Service  
```
VITE_API_URL=https://your-backend.up.railway.app
```

## Need the full guide?
See [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) for detailed instructions.
