import { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { Download, ArrowLeft, CheckCircle, Clock, Eye, User } from 'lucide-react';
import { downloadVideo, getFileUrl } from '../api/client';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedFormat, setSelectedFormat] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [downloadSuccess, setDownloadSuccess] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState('');
  const [thumbnailError, setThumbnailError] = useState(false);

  const videoData = location.state?.videoData;
  const url = location.state?.url;

  useEffect(() => {
    if (!videoData || !url) {
      navigate('/');
    }
  }, [videoData, url, navigate]);

  if (!videoData || !url) {
    return null;
  }

  const handleDownload = async () => {
    if (!selectedFormat) {
      setError('Please select a format');
      return;
    }

    setLoading(true);
    setError('');
    setDownloadSuccess(false);

    try {
      const isAudioOnly = selectedFormat === 'audio';
      const formatId = isAudioOnly ? null : selectedFormat;

      const result = await downloadVideo(url, formatId, isAudioOnly);

      if (result.status === 'success' && result.filename) {
        setDownloadSuccess(true);
        const fileUrl = getFileUrl(result.filename);
        setDownloadUrl(fileUrl);

        window.location.href = fileUrl;
      } else {
        setError('Download failed. Please try again.');
      }
    } catch (err) {
      setError(err.detail || 'Failed to download video. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 animate-fade-in">
      <div className="max-w-4xl mx-auto">
        {/* Back Button */}
        <Link
          to="/"
          className="inline-flex items-center px-4 py-2 bg-gray-100 dark:bg-emerald-900 hover:bg-gray-200 dark:hover:bg-emerald-800 text-gray-700 dark:text-gray-200 font-medium rounded-lg mb-6 transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Home
        </Link>

        {/* Video Info Card */}
        <div className="card p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-6">
            {/* Thumbnail */}
            <div className="md:w-1/3">
              {!thumbnailError && videoData.thumbnail ? (
                <img
                  src={videoData.thumbnail}
                  alt={videoData.title}
                  className="w-full rounded-lg border border-gray-200 dark:border-gray-800"
                  onError={() => setThumbnailError(true)}
                />
              ) : (
                <div className="w-full aspect-video bg-gray-100 dark:bg-emerald-900 rounded-lg border border-gray-200 dark:border-emerald-800 flex items-center justify-center">
                  <div className="text-center text-gray-500 dark:text-gray-400">
                    <svg className="w-16 h-16 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    <p className="text-sm font-medium">No preview</p>
                  </div>
                </div>
              )}
            </div>

            {/* Info */}
            <div className="md:w-2/3">
              <div className="flex items-start justify-between mb-4">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex-grow">
                  {videoData.title}
                </h2>
                <span className="ml-3 px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-lg text-sm font-semibold">
                  {videoData.platform}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {videoData.uploader && (
                  <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 text-sm">
                    <User className="w-4 h-4" />
                    <span>{videoData.uploader}</span>
                  </div>
                )}
                <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 text-sm">
                  <Clock className="w-4 h-4" />
                  <span>{videoData.duration_str}</span>
                </div>
                {videoData.view_count && (
                  <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 text-sm">
                    <Eye className="w-4 h-4" />
                    <span>{videoData.view_count.toLocaleString()} views</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Format Selection Card */}
        <div className="card p-6 mb-6">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Select Format & Quality
          </h3>

          <div className="space-y-2 mb-6">
            {videoData.formats && videoData.formats.length > 0 ? (
              videoData.formats.map((format, index) => (
                <label
                  key={index}
                  className={`flex items-center justify-between p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedFormat === format.format_id
                      ? 'border-green-500 bg-green-50 dark:bg-green-950/30'
                      : 'border-gray-200 dark:border-emerald-800 hover:border-gray-300 dark:hover:border-emerald-700'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <input
                      type="radio"
                      name="format"
                      value={format.format_id}
                      checked={selectedFormat === format.format_id}
                      onChange={(e) => setSelectedFormat(e.target.value)}
                      className="w-4 h-4 text-green-600 focus:ring-2 focus:ring-green-500"
                    />
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {format.quality}
                        {format.format_note && ` - ${format.format_note}`}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {format.ext.toUpperCase()}
                        {format.filesize_str && ` • ${format.filesize_str}`}
                      </p>
                    </div>
                  </div>
                  {selectedFormat === format.format_id && (
                    <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-500" />
                  )}
                </label>
              ))
            ) : (
              <p className="text-gray-500 dark:text-gray-400 text-center py-4">No formats available</p>
            )}
          </div>

          {error && (
            <div className="mb-4">
              <ErrorMessage message={error} onClose={() => setError('')} />
            </div>
          )}

          {downloadSuccess && (
            <div className="mb-4 bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800 rounded-lg p-4">
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-500" />
                <div>
                  <p className="font-semibold text-green-800 dark:text-green-400">Download Started!</p>
                  <p className="text-sm text-green-700 dark:text-green-500">
                    If download doesn't start,{' '}
                    <a
                      href={downloadUrl}
                      className="underline font-medium hover:text-green-900 dark:hover:text-green-300"
                      download
                    >
                      click here
                    </a>
                  </p>
                </div>
              </div>
            </div>
          )}

          <button
            onClick={handleDownload}
            disabled={loading || !selectedFormat}
            className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            <Download className="w-5 h-5" />
            <span>{loading ? 'Downloading...' : 'Download Video'}</span>
          </button>

          {loading && (
            <div className="mt-6">
              <LoadingSpinner message="Preparing your download..." />
            </div>
          )}
        </div>

        {/* Info Box */}
        <div className="bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <p className="text-sm text-green-800 dark:text-green-400">
            <strong>💡 Tip:</strong> Higher quality videos may take longer to download.
            Audio-only downloads are faster and smaller in size.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
