# Railway Deployment - Troubleshooting Guide

## Error: "Script start.sh not found" or "Railpack could not determine how to build"

This error occurs when Railway can't detect how to build your app. Here's how to fix it:

### ✅ **Solution 1: Verify Root Directory**

**Most Common Issue**: Root directory not set correctly.

1. Go to your Railway service
2. Click **Settings** → **Service Settings**
3. Under **Source**, set **Root Directory** to:
   - Backend service: `backend`
   - Frontend service: `frontend`
4. Click **Save**
5. Redeploy

### ✅ **Solution 2: Use Nixpacks Configuration**

Railway now uses **Nixpacks** by default. I've added configuration files:

**Backend:**
- ✅ `backend/nixpacks.toml` - Build configuration
- ✅ `backend/start.sh` - Start script
- ✅ `backend/Procfile` - Process file (backup)
- ✅ `backend/railway.json` - Railway settings

**Frontend:**
- ✅ `frontend/nixpacks.toml` - Build configuration  
- ✅ `frontend/start.sh` - Start script
- ✅ `frontend/railway.json` - Railway settings

### ✅ **Solution 3: Push Updated Config Files**

```bash
cd "D:\Video Downloader"
git add backend/nixpacks.toml backend/start.sh backend/railway.json
git add frontend/nixpacks.toml frontend/start.sh frontend/railway.json
git commit -m "Add Railway Nixpacks configuration"
git push origin main
```

### ✅ **Solution 4: Manually Set Build & Start Commands**

If automatic detection still fails, set commands manually in Railway dashboard:

#### Backend Service:
1. Go to service → **Settings** → **Deploy**
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Frontend Service:
1. Go to service → **Settings** → **Deploy**
2. **Build Command**: `npm install && npm run build`
3. **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

## Error: Build succeeds but app crashes

### Check Logs:
1. Go to your service in Railway
2. Click **Deployments** → Select latest deployment
3. Click **View Logs**
4. Look for error messages

### Common Issues:

**Missing Environment Variables:**
- Backend needs: `FRONTEND_URL`
- Frontend needs: `VITE_API_URL`

**Port Binding:**
- Make sure your app uses `$PORT` environment variable
- Backend: Uses `PORT` in main.py ✅
- Frontend: Uses `PORT` in preview command ✅

## Error: CORS issues after deployment

**Fix:**
1. Backend service → Variables
2. Add: `FRONTEND_URL` = your frontend Railway URL
3. Make sure frontend URL starts with `https://`
4. Redeploy backend

## Step-by-Step Deployment (After Config Fix)

### 1. Push Changes
```bash
git add .
git commit -m "Fix Railway configuration"
git push origin main
```

### 2. Deploy Backend
1. Railway → **New Project** → **Deploy from GitHub**
2. Select repository
3. **Settings** → Set Root Directory: `backend`
4. Deploy will start automatically
5. Wait for "Deployed" status
6. Copy backend URL

### 3. Deploy Frontend  
1. Same project → **+ New** → **GitHub Repo**
2. Select same repository
3. **Settings** → Set Root Directory: `frontend`
4. **Variables** → Add `VITE_API_URL` = backend URL
5. Deploy automatically
6. Copy frontend URL

### 4. Link Services
1. Backend service → **Variables**
2. Add `FRONTEND_URL` = frontend URL
3. Save (auto-redeploys)

## Still Having Issues?

### Option 1: Deploy with Dockerfile (Alternative)

If Nixpacks continues to fail, Railway also supports Docker:

1. The project includes `backend/Dockerfile`
2. Railway will auto-detect and use it
3. Remove or rename `nixpacks.toml` to force Docker build

### Option 2: Check Railway Status

- Visit: https://railway.statuspage.io/
- Check if there are any ongoing incidents

### Option 3: Railway Community

- Discord: https://discord.gg/railway
- Community Forum: https://help.railway.app/

## Files Created for Railway Support

| File | Purpose |
|------|---------|
| `backend/nixpacks.toml` | Nixpacks build configuration |
| `backend/start.sh` | Startup script |
| `backend/Procfile` | Process definition (Heroku-style) |
| `backend/railway.json` | Railway-specific settings |
| `frontend/nixpacks.toml` | Nixpacks build configuration |
| `frontend/start.sh` | Startup script |
| `frontend/railway.json` | Railway-specific settings |

All configuration methods are included so Railway can detect one of them!
