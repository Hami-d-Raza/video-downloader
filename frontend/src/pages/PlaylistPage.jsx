import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Download, Clock, User, Video } from 'lucide-react';
import { analyzeVideo } from '../api/client';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const PlaylistPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { playlist } = location.state || {};

  const [selectedVideos, setSelectedVideos] = useState(new Set());
  const [processing, setProcessing] = useState(false);

  if (!playlist) {
    return (
      <div className="container mx-auto px-4 py-8">
        <ErrorMessage message="No playlist data found. Please go back and analyze a playlist." />
      </div>
    );
  }

  const toggleVideo = (videoId) => {
    const newSelected = new Set(selectedVideos);
    if (newSelected.has(videoId)) {
      newSelected.delete(videoId);
    } else {
      newSelected.add(videoId);
    }
    setSelectedVideos(newSelected);
  };

  const selectAll = () => {
    if (selectedVideos.size === playlist.videos.length) {
      setSelectedVideos(new Set());
    } else {
      setSelectedVideos(new Set(playlist.videos.map(v => v.id)));
    }
  };

  const handleDownloadSelected = async () => {
    if (selectedVideos.size === 0) {
      alert('Please select at least one video');
      return;
    }

    const selectedVideoData = playlist.videos.filter(v => selectedVideos.has(v.id));
    
    // Navigate to batch download page
    if (selectedVideoData.length > 0) {
      try {
        setProcessing(true);
        
        // Get detailed info for the first video to determine available formats
        const firstVideo = selectedVideoData[0];
        const videoData = await analyzeVideo(firstVideo.url);
        
        // Navigate to results page with batch mode enabled
        navigate('/results', {
          state: {
            videoData,
            batchMode: true,
            batchUrls: selectedVideoData.map(v => v.url),
            batchCount: selectedVideoData.length,
            playlistTitle: playlist.title
          }
        });
      } catch (error) {
        alert(`Error: ${error.detail || 'Failed to analyze video'}`);
      } finally {
        setProcessing(false);
      }
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Playlist Header */}
      <div className="card p-6 mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
          {playlist.title}
        </h1>
        
        <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400">
          {playlist.uploader && (
            <div className="flex items-center gap-1.5">
              <User className="w-4 h-4" />
              <span>{playlist.uploader}</span>
            </div>
          )}
          <div className="flex items-center gap-1.5">
            <Video className="w-4 h-4" />
            <span>{playlist.video_count} videos</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="px-2 py-0.5 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded text-xs font-medium">
              {playlist.platform}
            </span>
          </div>
        </div>
      </div>

      {/* Selection Controls */}
      <div className="card p-4 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={selectAll}
              className="text-sm text-green-600 dark:text-green-400 hover:underline"
            >
              {selectedVideos.size === playlist.videos.length ? 'Deselect All' : 'Select All'}
            </button>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {selectedVideos.size} of {playlist.video_count} selected
            </span>
          </div>
          
          <button
            onClick={handleDownloadSelected}
            disabled={selectedVideos.size === 0 || processing}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {processing ? (
              <>
                <LoadingSpinner />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>Download Selected</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Video List */}
      <div className="space-y-3">
        {playlist.videos.map((video, index) => (
          <div
            key={video.id}
            className={`card p-4 cursor-pointer transition-all ${
              selectedVideos.has(video.id)
                ? 'ring-2 ring-green-500 dark:ring-green-600'
                : 'hover:shadow-md'
            }`}
            onClick={() => toggleVideo(video.id)}
          >
            <div className="flex items-start gap-4">
              {/* Checkbox */}
              <div className="flex-shrink-0 pt-1">
                <input
                  type="checkbox"
                  checked={selectedVideos.has(video.id)}
                  onChange={() => toggleVideo(video.id)}
                  className="w-5 h-5 text-green-600 rounded border-gray-300 dark:border-emerald-700 focus:ring-green-500"
                  onClick={(e) => e.stopPropagation()}
                />
              </div>

              {/* Thumbnail */}
              {video.thumbnail && (
                <div className="flex-shrink-0">
                  <img
                    src={video.thumbnail}
                    alt={video.title}
                    className="w-40 h-24 object-cover rounded"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                </div>
              )}

              {/* Video Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h3 className="font-medium text-gray-900 dark:text-white line-clamp-2">
                    {index + 1}. {video.title}
                  </h3>
                  {video.duration_str && (
                    <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-400 flex-shrink-0">
                      <Clock className="w-4 h-4" />
                      <span>{video.duration_str}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {playlist.videos.length === 0 && (
        <div className="card p-8 text-center">
          <p className="text-gray-600 dark:text-gray-400">No videos found in this playlist.</p>
        </div>
      )}
    </div>
  );
};

export default PlaylistPage;
