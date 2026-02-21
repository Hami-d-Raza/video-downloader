# Railway Backend Deployment - Manual Setup Instructions

## ⚠️ If Auto-Detection Fails

If Railway shows "Script start.sh not found" or build errors, follow these **manual configuration steps**:

### Step 1: Deploy from GitHub

1. Go to https://railway.app/new
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. **CRITICAL**: Before deploying, click **"Configure"** or go to **Settings**

### Step 2: Set Root Directory

1. In Railway service settings
2. Find **"Source"** section
3. Set **Root Directory** to: `backend`
4. Save

### Step 3: Manual Build Configuration

Since auto-detection isn't working, set these manually:

#### Option A: Use Railway Dashboard (Recommended)

1. Go to your Railway service → **Settings**
2. Scroll to **"Build"** section
3. Set these values:

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

4. Click **Save**
5. Click **"Deploy"** to trigger new deployment

#### Option B: Use Environment Variables

If the above doesn't work, Railway might be looking for these variables:

1. Go to **Variables** tab
2. Add these:

```
NIXPACKS_BUILD_CMD=pip install -r requirements.txt
NIXPACKS_START_CMD=uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 4: Add Your Vercel URL

In **Variables** tab, add:

```
FRONTEND_URL=https://your-app.vercel.app
```

Replace with your actual Vercel URL.

### Step 5: Verify Deployment

After deployment:

1. Check **Deployments** tab → **Build Logs**
2. Look for successful pip install
3. Check **Deploy Logs** for uvicorn starting
4. Test the URL: `https://your-backend.up.railway.app/`

You should see:
```json
{
  "status": "online",
  "message": "Video Downloader API is running",
  "version": "1.0.0"
}
```

## 🔧 Alternative: Use Railway CLI

If the dashboard isn't working, try Railway CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Set root directory
railway up --rootDir backend

# Set environment variable
railway variables set FRONTEND_URL=https://your-app.vercel.app
```

## 📋 Files in Backend Folder

These files help Railway detect your app:

| File | Purpose | Status |
|------|---------|--------|
| `requirements.txt` | Python dependencies | ✅ Required |
| `Procfile` | Process definition (Heroku-style) | ✅ Used |
| `nixpacks.toml` | Nixpacks configuration | ✅ Used |
| `railway.json` | Railway settings | ✅ Used |
| `.python-version` | Python version | ✅ Used |
| `main.py` | FastAPI app entry point | ✅ Required |

## 🐛 Common Issues & Solutions

### Issue: "No module named 'fastapi'"

**Cause**: Dependencies not installed

**Fix**: Make sure Build Command includes:
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"

**Cause**: Port conflict

**Fix**: Start command must use `$PORT`:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Issue: "Service crashes immediately"

**Check logs**:
1. Railway → Deployments → Latest → **Deploy Logs**
2. Look for Python errors

**Common fixes**:
- Verify all environment variables are set
- Check that `main.py` exists in backend folder
- Ensure Root Directory is set to `backend`

### Issue: CORS errors from Vercel

**Fix**: Make sure `FRONTEND_URL` is set in Railway Variables

### Issue: Build works but 404 on all endpoints

**Cause**: Root directory not set

**Fix**: Railway Settings → Source → Root Directory = `backend`

## ✅ Verification Steps

1. **Check Railway Dashboard**:
   - Service shows "Active" status
   - Recent deployment succeeded
   - Logs show "Uvicorn running on 0.0.0.0:XXXX"

2. **Test Health Endpoint**:
   ```bash
   curl https://your-backend.up.railway.app/
   ```
   Should return JSON with status "online"

3. **Test from Vercel**:
   - Open Vercel frontend
   - Paste a YouTube video URL
   - Click "Analyze Video"
   - Should show video info (not CORS error)

## 📞 Need Help?

If manual setup still doesn't work:

1. **Check Railway Status**: https://railway.statuspage.io/
2. **Railway Discord**: https://discord.gg/railway
3. **Railway Docs**: https://docs.railway.app/

## 🎯 Success Checklist

- [ ] Root Directory set to `backend`
- [ ] Build Command set (manually in dashboard)
- [ ] Start Command set (manually in dashboard)  
- [ ] `FRONTEND_URL` environment variable added
- [ ] Deployment succeeded (green checkmark)
- [ ] Health endpoint returns 200 OK
- [ ] Vercel frontend can connect (no CORS errors)
- [ ] Video download works end-to-end

Once all checked, your backend is live! 🚀
