import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Youtube, Facebook, Instagram, Music2, Search, ArrowRight } from 'lucide-react';
import { analyzeVideo } from '../api/client';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const HomePage = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!url.trim()) {
      setError('Please enter a video URL');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await analyzeVideo(url);
      
      navigate('/results', { 
        state: { 
          videoData: data,
          url: url 
        } 
      });
    } catch (err) {
      setError(err.detail || 'Failed to analyze video. Please check the URL and try again.');
    } finally {
      setLoading(false);
    }
  };

  const supportedPlatforms = [
    { name: 'YouTube', icon: Youtube, color: 'text-red-600 dark:text-red-500', bg: 'bg-red-50 dark:bg-red-950/30' },
    { name: 'Facebook', icon: Facebook, color: 'text-blue-600 dark:text-blue-500', bg: 'bg-blue-50 dark:bg-blue-950/30' },
    { name: 'Instagram', icon: Instagram, color: 'text-pink-600 dark:text-pink-500', bg: 'bg-pink-50 dark:bg-pink-950/30' },
    { name: 'TikTok', icon: Music2, color: 'text-gray-900 dark:text-gray-400', bg: 'bg-gray-50 dark:bg-emerald-900' },
  ];

  const features = [
    { title: 'Multiple Formats', description: 'Choose from various video qualities', emoji: '🎬' },
    { title: 'Audio Only', description: 'Extract audio as MP3', emoji: '🎵' },
    { title: 'Fast & Free', description: 'Quick downloads at no cost', emoji: '⚡' },
  ];

  return (
    <div className="container mx-auto px-4 py-12 animate-fade-in">
      <div className="max-w-3xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900 dark:text-white">
            Download Videos Instantly
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Save videos from YouTube, Facebook, Instagram, and TikTok in high quality
          </p>
        </div>

        {/* Main Form */}
        <div className="card p-6 mb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="url" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Video URL
              </label>
              <div className="relative">
                <input
                  id="url"
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="input-field pr-12"
                  disabled={loading}
                />
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <Search className="w-5 h-5 text-gray-400" />
                </div>
              </div>
            </div>

            {error && (
              <ErrorMessage message={error} onClose={() => setError('')} />
            )}

            <button
              type="submit"
              disabled={loading || !url.trim()}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <span>Analyze Video</span>
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>

          {loading && (
            <div className="mt-6">
              <LoadingSpinner message="Fetching video information..." />
            </div>
          )}
        </div>

        {/* Supported Platforms */}
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 text-center">
            Supported Platforms
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {supportedPlatforms.map((platform) => (
              <div
                key={platform.name}
                className={`flex flex-col items-center p-4 rounded-lg ${platform.bg} border border-gray-200 dark:border-emerald-800 hover:border-gray-300 dark:hover:border-emerald-700 transition-colors`}
              >
                <platform.icon className={`w-8 h-8 ${platform.color} mb-2`} />
                <p className="font-medium text-gray-900 dark:text-gray-100 text-sm">{platform.name}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-4">
          {features.map((feature, index) => (
            <div key={index} className="card p-5 text-center hover:border-gray-300 dark:hover:border-emerald-700 transition-colors">
              <div className="text-3xl mb-3">{feature.emoji}</div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-1">{feature.title}</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;
