# Video Downloader Frontend

Modern React frontend for the Video Downloader application.

## Features

- ✅ Clean, modern UI with Tailwind CSS
- ✅ Responsive design (mobile-friendly)
- ✅ Real-time video analysis
- ✅ Multiple format selection
- ✅ Loading states and error handling
- ✅ Platform detection
- ✅ Audio-only download option

## Prerequisites

- Node.js 18+ 
- npm or yarn

## Installation

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Update `.env` with your backend URL:
```env
VITE_API_URL=http://localhost:8000
```

## Running the Application

### Development
```bash
npm run dev
```

The app will start at `http://localhost:5173`

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/
│   │   └── client.js    # API client with axios
│   ├── components/
│   │   ├── Header.jsx   # Header component
│   │   ├── Footer.jsx   # Footer with disclaimer
│   │   ├── LoadingSpinner.jsx
│   │   └── ErrorMessage.jsx
│   ├── pages/
│   │   ├── HomePage.jsx    # Main landing page
│   │   └── ResultsPage.jsx # Video results & download
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind configuration
└── postcss.config.js    # PostCSS configuration
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Technology Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Routing
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons

## Features

### Home Page
- URL input field
- Platform detection
- Supported platforms showcase
- Features overview

### Results Page
- Video thumbnail and metadata
- Multiple format options
- Quality selection
- Download button
- Progress indicators

### Components
- **Header** - Navigation and branding
- **Footer** - Disclaimer and legal info
- **LoadingSpinner** - Loading states
- **ErrorMessage** - Error handling

## API Integration

The frontend communicates with the backend through REST API:

```javascript
import { analyzeVideo, downloadVideo } from './api/client';

// Analyze video
const videoData = await analyzeVideo(url);

// Download video
const result = await downloadVideo(url, formatId, audioOnly);
```

## Styling

### Tailwind CSS Classes

Custom utility classes defined in `index.css`:

- `.btn-primary` - Primary button style
- `.btn-secondary` - Secondary button style
- `.input-field` - Input field style
- `.card` - Card container style

### Color Scheme

- Primary: Blue (`primary-500`)
- Success: Green
- Error: Red
- Warning: Yellow

## Responsive Design

- Mobile-first approach
- Breakpoints:
  - `sm`: 640px
  - `md`: 768px
  - `lg`: 1024px
  - `xl`: 1280px

## Configuration

### Vite Configuration

`vite.config.js` includes:
- React plugin
- Proxy to backend API
- Port configuration

### Tailwind Configuration

`tailwind.config.js` includes:
- Custom color palette
- Content paths
- Theme extensions

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Environment Variables

```env
VITE_API_URL=http://localhost:8000  # Backend API URL
```

## Deployment

### Build
```bash
npm run build
```

The `dist/` folder contains production-ready files.

### Static Hosting

Deploy to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

### Environment Variables in Production

Set `VITE_API_URL` to your production backend URL.

## Troubleshooting

### Port already in use
Change port in `vite.config.js`:
```javascript
server: {
  port: 3000
}
```

### API connection errors
- Check backend is running
- Verify `VITE_API_URL` in `.env`
- Check CORS settings in backend

### Build errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Best Practices

- ✅ Component-based architecture
- ✅ Responsive design
- ✅ Error boundaries
- ✅ Loading states
- ✅ Accessibility
- ✅ Clean code structure

## License

For educational purposes only.
