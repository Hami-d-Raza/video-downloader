# Deploy Backend to Railway (Frontend on Vercel)

Since you've already deployed your frontend on Vercel, here's how to deploy just the backend to Railway.

## 🚀 Quick Deployment Steps

### Step 1: Deploy Backend to Railway

1. Go to https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Select your **video-downloader** repository
4. ⚠️ **CRITICAL**: Click **Settings** → **Source** → Set **Root Directory** to:
   ```
   backend
   ```
5. Click **Deploy**

### Step 2: Configure Environment Variables

Once deployed, add your Vercel frontend URL:

1. Go to your Railway backend service
2. Click **Variables** tab
3. Add a new variable:
   - **Key**: `FRONTEND_URL`
   - **Value**: `https://your-app.vercel.app` (your Vercel URL)
4. Click **Add** and save

Example:
```
FRONTEND_URL=https://video-downloader-frontend.vercel.app
```

### Step 3: Update Vercel Frontend

Update your Vercel frontend environment variable:

1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Update `VITE_API_URL` to your Railway backend URL:
   ```
   VITE_API_URL=https://your-backend.up.railway.app
   ```
4. **Redeploy** your Vercel frontend

### Step 4: Test the Connection

1. Open your Vercel frontend URL
2. Try analyzing a video
3. Check browser console for any CORS errors
4. If you see errors, verify:
   - `FRONTEND_URL` is set correctly in Railway
   - `VITE_API_URL` is set correctly in Vercel
   - Both URLs use `https://` (no trailing slash)

## 📋 Configuration Details

### Railway Backend Configuration Files

The backend includes multiple configuration methods:

- ✅ `backend/nixpacks.toml` - Primary build config
- ✅ `backend/railway.json` - Railway settings
- ✅ `backend/start.sh` - Startup script
- ✅ `backend/Procfile` - Process definition

### Environment Variables

| Variable | Value | Required |
|----------|-------|----------|
| `FRONTEND_URL` | Your Vercel frontend URL | Yes |
| `PORT` | Auto-set by Railway | Auto |

### CORS Configuration

The backend is configured to automatically allow:
- ✅ Your Vercel URL (via `FRONTEND_URL` env var)
- ✅ All `*.vercel.app` domains (for preview deployments)
- ✅ Local development URLs (`localhost:5173`, etc.)

## 🔧 Troubleshooting

### Error: "Script start.sh not found"

**Fix**: Make sure **Root Directory** is set to `backend` in Railway settings.

1. Railway service → **Settings**
2. **Source** section → **Root Directory** → `backend`
3. **Save** and redeploy

### Error: CORS policy blocking requests

**Fix**: Check environment variables

1. **Railway backend** must have `FRONTEND_URL` set to your Vercel URL
2. **Vercel frontend** must have `VITE_API_URL` set to your Railway URL
3. Make sure URLs:
   - Start with `https://`
   - Don't have trailing slashes
   - Are the production URLs (not localhost)

Example:
```bash
# Correct ✅
FRONTEND_URL=https://my-app.vercel.app
VITE_API_URL=https://my-backend.up.railway.app

# Wrong ❌
FRONTEND_URL=https://my-app.vercel.app/
VITE_API_URL=http://my-backend.up.railway.app
```

### Build fails on Railway

**Check build logs**:
1. Railway service → **Deployments**
2. Click latest deployment
3. View **Build Logs**

**Common issues**:
- Root directory not set to `backend`
- Missing `requirements.txt`
- Python version incompatibility

**Fix**: Ensure `backend/nixpacks.toml` specifies Python 3.9:
```toml
[phases.setup]
nixPkgs = ["python39", "ffmpeg", "gcc"]
```

### Backend starts but crashes

**Check runtime logs**:
1. Railway service → **Deployments**
2. Click **View Logs**
3. Look for Python errors

**Common causes**:
- Missing dependencies in `requirements.txt`
- Port not binding correctly (should use `$PORT`)
- Missing environment variables

### API requests timeout

**Increase timeout in Vercel frontend**:

The `frontend/src/api/client.js` already has a 10-minute timeout:
```javascript
timeout: 600000, // 10 minutes
```

If needed, adjust in Railway too by checking service health.

## 🎯 Verification Checklist

After deployment, verify:

- [ ] Railway backend is deployed and running
- [ ] Railway backend URL copied (e.g., `https://xxx.up.railway.app`)
- [ ] `FRONTEND_URL` set in Railway to your Vercel URL
- [ ] `VITE_API_URL` set in Vercel to your Railway backend URL
- [ ] Vercel frontend redeployed after environment variable change
- [ ] Test video download on Vercel frontend works
- [ ] No CORS errors in browser console

## 📊 Expected URLs

| Service | Platform | Example URL |
|---------|----------|-------------|
| Frontend | Vercel | `https://video-downloader.vercel.app` |
| Backend API | Railway | `https://video-downloader-backend.up.railway.app` |

## 💡 Tips

### For Multiple Vercel Deployments

If you have preview deployments on Vercel, add them to `FRONTEND_URL`:

```
FRONTEND_URL=https://video-downloader.vercel.app,https://video-downloader-preview.vercel.app
```

Use commas to separate multiple URLs.

### Monitor Railway Usage

- Railway free tier: $5/month credit
- Check usage: Railway dashboard → Project → **Usage**
- Backend typically uses ~$5-10/month

### View Backend Logs

Monitor your backend in real-time:

1. Railway service → **Deployments**
2. Click latest deployment → **View Logs**
3. Watch for errors or successful requests

## 🆘 Still Having Issues?

1. Check [RAILWAY_TROUBLESHOOTING.md](./RAILWAY_TROUBLESHOOTING.md)
2. Verify both environment variables are set correctly
3. Check Railway deployment logs
4. Test backend API directly: `https://your-backend.up.railway.app/`
5. Join Railway Discord: https://discord.gg/railway

## ✅ Success!

Once deployed:
- Your backend runs on Railway
- Your frontend runs on Vercel
- They communicate via HTTPS
- CORS is properly configured
- You can download videos! 🎉
