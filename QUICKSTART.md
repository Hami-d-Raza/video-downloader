# 🚀 Quick Start Guide

Get your Video Downloader up and running in minutes!

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8 or higher
- [ ] Node.js 18 or higher  
- [ ] FFmpeg installed

### Quick Check Commands

```powershell
# Windows PowerShell
python --version    # Should show 3.8+
node --version      # Should show 18+
ffmpeg -version     # Should show FFmpeg info
```

---

## Option 1: Automated Setup (Recommended)

### Windows
```powershell
.\setup.ps1
```

### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

Then follow the printed instructions to start the servers.

---

## Option 2: Manual Setup

### Step 1: Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Start the server
python main.py
```

✅ Backend running at: http://localhost:8000

### Step 2: Frontend Setup

Open a **new terminal**:

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm run dev
```

✅ Frontend running at: http://localhost:5173

---

## Option 3: Docker Setup

```bash
# Build and run containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

## Verify Installation

1. **Backend**: Open http://localhost:8000 - Should show API status
2. **Frontend**: Open http://localhost:5173 - Should show the app
3. **API Docs**: Open http://localhost:8000/docs - Interactive API documentation

---

## First Download Test

1. Go to http://localhost:5173
2. Paste a YouTube URL (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)
3. Click "Analyze Video"
4. Select a format
5. Click "Download Video"

---

## Common Issues

### FFmpeg Not Found
```powershell
# Windows (using Chocolatey)
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

### Port Already in Use

**Backend (8000):**
Edit `backend/.env`:
```env
PORT=8001
```

**Frontend (5173):**
Edit `frontend/vite.config.js`:
```javascript
server: { port: 3000 }
```

### Module Not Found

**Backend:**
```powershell
cd backend
pip install -r requirements.txt
```

**Frontend:**
```powershell
cd frontend
npm install
```

### Can't Connect to Backend

1. Verify backend is running: http://localhost:8000
2. Check `frontend/.env`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
3. Restart frontend after changing .env

---

## Development Tips

### Backend Hot Reload
```powershell
# Use uvicorn with reload
uvicorn main:app --reload
```

### Frontend Hot Reload
Vite automatically reloads on file changes!

### View Logs

**Backend:** Check terminal running `python main.py`
**Frontend:** Check terminal running `npm run dev`

---

## Production Build

### Backend
```powershell
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```powershell
cd frontend
npm run build
# Deploy the 'dist' folder
```

---

## Next Steps

- [ ] Read the [Main README](README.md) for full documentation
- [ ] Check [Backend README](backend/README.md) for API details
- [ ] Check [Frontend README](frontend/README.md) for UI customization
- [ ] Test different video platforms
- [ ] Customize styling (Tailwind CSS in frontend)
- [ ] Add rate limiting configuration

---

## Support

**📁 Documentation:**
- Main README: [README.md](README.md)
- Backend docs: [backend/README.md](backend/README.md)
- Frontend docs: [frontend/README.md](frontend/README.md)

**🔧 Troubleshooting:**
See the Troubleshooting sections in the README files

**🎯 API Documentation:**
http://localhost:8000/docs (when backend is running)

---

## Platform URLs for Testing

**YouTube:**
- https://www.youtube.com/watch?v={VIDEO_ID}
- https://youtu.be/{VIDEO_ID}

**TikTok:**
- https://www.tiktok.com/@{username}/video/{VIDEO_ID}

**Instagram:**
- https://www.instagram.com/p/{POST_ID}/
- https://www.instagram.com/reel/{REEL_ID}/

**Facebook:**
- https://www.facebook.com/watch/?v={VIDEO_ID}
- https://fb.watch/{VIDEO_ID}

---

**Happy Downloading! 🎬**

Remember: Only download content you have rights to access!
