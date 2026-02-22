# 🎬 Video Downloader

A production-ready web application for downloading videos from YouTube, Facebook, Instagram, and TikTok. Built with FastAPI (backend) and React (frontend).

![License](https://img.shields.io/badge/license-Educational-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![React](https://img.shields.io/badge/react-18-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.109-green)
![Production Ready](https://img.shields.io/badge/production-ready-brightgreen)

## 🌟 Live Demo

- **Frontend**: https://video-downloader-jade.vercel.app
- **Backend API**: https://video-downloader-production-e4fe.up.railway.app

## 📖 Quick Links

- **[🚀 Deployment Guide](DEPLOYMENT_GUIDE.md)** - Complete guide to deploy to Vercel
- **[✅ Production Checklist](PRODUCTION_CHECKLIST.md)** - Production readiness checklist
- **[📚 API Documentation](https://video-downloader-production-e4fe.up.railway.app/docs)** - Interactive API docs

---

## ⚠️ Important Disclaimer

**Users must have rights to download content. Only publicly accessible content is supported. Please respect copyright and platform terms of service.**

This application is for educational purposes only.

---

## 🎯 Features

### Backend
- ✅ Multi-platform support (YouTube, Facebook, Instagram, TikTok)
- ✅ Multiple video quality options (360p, 720p, 1080p, etc.)
- ✅ Audio-only download (MP3 extraction)
- ✅ Automatic platform detection
- ✅ Rate limiting to prevent abuse
- ✅ Automatic file cleanup
- ✅ Comprehensive error handling
- ✅ REST API with FastAPI

### Frontend
- ✅ Modern, responsive UI with Tailwind CSS
- ✅ Real-time video analysis
- ✅ Format and quality selection
- ✅ Loading states and progress indicators
- ✅ Error handling with user-friendly messages
- ✅ Mobile-friendly design
- ✅ Platform detection and validation

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **yt-dlp** - Video extraction
- **FFmpeg** - Media processing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide React** - Icons

---

## 📋 Prerequisites

### System Requirements
- **Python 3.8+**
- **Node.js 18+**
- **FFmpeg** (required for video processing)

### Installing FFmpeg

**Windows:**
```powershell
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Video Downloader"
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run the server
python main.py
```

Backend runs at: **http://localhost:8000**

### 3. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## 📁 Project Structure

```
video-downloader/
├── backend/               # FastAPI backend (Railway)
│   ├── main.py           # FastAPI application
│   ├── downloader.py     # Video downloader module
│   ├── utils.py          # Utility functions
│   ├── requirements.txt  # Python dependencies
│   ├── railway.json      # Railway configuration
│   └── .env.example
│
├── frontend/             # React frontend (Vercel)
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js     # API client
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ErrorMessage.jsx
│   │   ├── context/
│   │   │   └── ThemeContext.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ResultsPage.jsx
│   │   │   └── PlaylistPage.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json       # Vercel configuration
│   ├── .vercelignore     # Vercel ignore file
│   └── .env.example
│
├── DEPLOYMENT_GUIDE.md   # 📖 Complete deployment guide
├── PRODUCTION_CHECKLIST.md
└── README.md             # This file
```

---

## 🎮 Usage

### Step 1: Access the Application
Open your browser and go to `http://localhost:5173`

### Step 2: Paste Video URL
Enter a video URL from:
- YouTube (youtube.com, youtu.be)
- Facebook (facebook.com, fb.watch)
- Instagram (instagram.com)
- TikTok (tiktok.com)

### Step 3: Analyze Video
Click "Analyze Video" to fetch video information

### Step 4: Select Format
Choose your preferred:
- Video quality (360p, 720p, 1080p, etc.)
- Audio only (MP3)

### Step 5: Download
Click "Download Video" to start the download

---

## 🔌 API Documentation

### Backend Endpoints

#### GET /
Health check
```bash
curl http://localhost:8000/
```

#### POST /api/analyze
Analyze video URL
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=..."}'
```

#### POST /api/download
Download video
```bash
curl -X POST http://localhost:8000/api/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=...",
    "format_id": "137",
    "audio_only": false
  }'
```

#### GET /api/file/{filename}
Download file
```bash
curl http://localhost:8000/api/file/{filename} -O
```

Full API docs available at: `http://localhost:8000/docs`

---

## ⚙️ Configuration

### Backend (.env)
```env
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
MAX_FILE_AGE_HOURS=1
DOWNLOAD_DIR=./downloads
MAX_REQUESTS_PER_MINUTE=20
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🚀 Production Deployment

### Deploy to Vercel + Railway

This project is production-ready and optimized for deployment!

**📖 Complete Deployment Guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Quick Overview:**
1. **Backend**: Already deployed on Railway
   - URL: `https://video-downloader-production-e4fe.up.railway.app`
   
2. **Frontend**: Deploy to Vercel
   - Set Root Directory to `frontend`
   - Add environment variable: `VITE_API_URL`
   - One-click deploy from GitHub

**Production Checklist**: See [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)

### Environment Variables

**Vercel (Frontend)**:
```env
VITE_API_URL=https://video-downloader-production-e4fe.up.railway.app
```

**Railway (Backend)**:
```env
FRONTEND_URL=https://your-vercel-url.vercel.app
```

---

## 🏗️ Building for Production

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
cd frontend
npm run build
```

Build outputs to `dist/` folder (optimized and minified).

**Build Features**:
- Code splitting and lazy loading
- Minification and compression
- Source map removal for production
- Optimized chunk sizes

---

## 📦 Production Optimizations

### Frontend
- ✅ Vite production build with code splitting
- ✅ React vendor chunks separated
- ✅ Environment variable validation
- ✅ SEO meta tags optimized
- ✅ .vercelignore configured
- ✅ Bundle size optimized (< 500KB)

### Backend
- ✅ CORS configured for production domains
- ✅ Rate limiting enabled
- ✅ Auto file cleanup
- ✅ Health check endpoint
- ✅ Comprehensive logging

---

## 🔒 Security Features

- ✅ URL validation
- ✅ Platform verification
- ✅ Rate limiting (20 requests/minute)
- ✅ Input sanitization
- ✅ Automatic file cleanup
- ✅ CORS protection
- ✅ Error handling

---

## 🐛 Troubleshooting

### FFmpeg not found
```bash
# Install FFmpeg (see Prerequisites section)
ffmpeg -version
```

### Backend port in use
```bash
# Change port in backend/.env
PORT=8001
```

### Frontend can't connect to backend
1. Check backend is running: `http://localhost:8000`
2. Verify `VITE_API_URL` in `frontend/.env`
3. Check CORS settings in `backend/main.py`

### yt-dlp errors
```bash
# Update yt-dlp
pip install --upgrade yt-dlp
```

### Module not found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

---

## 📊 Features Roadmap

- [x] Basic video download
- [x] Multi-platform support
- [x] Audio extraction
- [x] Format selection
- [x] Rate limiting
- [ ] Download progress bar
- [ ] Batch downloads
- [ ] Download history
- [ ] User authentication
- [ ] Playlist support

---

## 🤝 Contributing

This is an educational project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is for **educational purposes only**.

**Important Legal Notes:**
- Respect platform terms of service
- Only download content you have rights to
- Don't use for commercial purposes
- Respect copyright laws

---

## 🙏 Acknowledgments

- **yt-dlp** - Powerful video downloader
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **Tailwind CSS** - Utility-first CSS framework

---

## 📧 Support

For issues and questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review backend/frontend README files
3. Check existing issues

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Built with ❤️ using FastAPI and React**

