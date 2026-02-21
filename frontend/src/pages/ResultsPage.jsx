import { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { Download, ArrowLeft, CheckCircle, Clock, Eye, User, Package } from 'lucide-react';
import { downloadVideo, downloadBatch, getFileUrl } from '../api/client';
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
  
  // Batch mode support
  const isBatchMode = location.state?.batchMode || false;
  const batchUrls = location.state?.batchUrls || [];
  const batchCount = location.state?.batchCount || 0;
  const playlistTitle = location.state?.playlistTitle || '';

  const videoData = location.state?.videoData;
  const url = location.state?.url;

  useEffect(() => {
    if (!videoData) {
      navigate('/');
    }
  }, [videoData, navigate]);

  if (!videoData) {
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

      let result;
      
      if (isBatchMode) {
        // Batch download - download all videos as ZIP
        result = await downloadBatch(batchUrls, formatId, isAudioOnly);
      } else {
        // Single video download
        result = await downloadVideo(url, formatId, isAudioOnly);
      }

      if (result.status === 'success' && result.filename) {
        setDownloadSuccess(true);
        const fileUrl = getFileUrl(result.filename);
        setDownloadUrl(fileUrl);

        // Trigger automatic download
        window.location.href = fileUrl;
        setLoading(false);
      } else {
        setError('Download failed. Please try again.');
        setLoading(false);
      }
    } catch (err) {
      setError(err.detail || 'Failed to download. Please try again.');
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

        {/* Batch Mode Indicator */}
        {isBatchMode && (
          <div className="card p-4 mb-4 bg-green-50 dark:bg-green-950/30 border-green-200 dark:border-green-800">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-green-600 text-white flex items-center justify-center">
                  <Package className="w-6 h-6" />
                </div>
                <div>
                  <p className="font-semibold text-green-900 dark:text-green-300">
                    Batch Download Mode
                  </p>
                  <p className="text-sm text-green-700 dark:text-green-400">
                    {batchCount} videos selected from "{playlistTitle}"
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-xl font-bold text-green-800 dark:text-green-400">
                  {batchCount}
                </p>
                <p className="text-xs text-green-600 dark:text-green-500">videos</p>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t border-green-200 dark:border-green-800">
              <p className="text-sm text-green-800 dark:text-green-400">
                📦 All videos will be downloaded in a single ZIP file
              </p>
            </div>
          </div>
        )}

        {/* Content Info Card */}
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
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Select Format & Quality
          </h3>
          
          {isBatchMode ? (
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              ⚠️ <strong>Batch Download:</strong> All {batchCount} videos will be downloaded in the selected quality and packaged as a ZIP file. Large batches may take 5-30 minutes.
            </p>
          ) : (
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              ⚠️ <strong>Note:</strong> Large files (HD/4K) may take 2-10 minutes to process. Please be patient.
            </p>
          )}

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
            <div className="mb-4 bg-green-50 dark:bg-green-950/30 border-2 border-green-500 dark:border-green-600 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-500 flex-shrink-0 mt-0.5" />
                <div>
                  {isBatchMode ? (
                    <>
                      <p className="font-bold text-green-800 dark:text-green-400 text-lg mb-1">ZIP Download Ready!</p>
                      <p className="text-sm text-green-700 dark:text-green-500 mb-2">
                        Your ZIP file with {batchCount} videos is ready! Download should start automatically.
                      </p>
                    </>
                  ) : (
                    <>
                      <p className="font-bold text-green-800 dark:text-green-400 text-lg mb-1">Download Ready!</p>
                      <p className="text-sm text-green-700 dark:text-green-500 mb-2">
                        Your download should start automatically.
                      </p>
                    </>
                  )}
                  <p className="text-sm text-green-700 dark:text-green-500">
                    If it doesn't start,{' '}
                    <a
                      href={downloadUrl}
                      className="underline font-semibold hover:text-green-900 dark:hover:text-green-300"
                      download
                    >
                      click here to download manually
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
                {loading ? (
                  <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>
                  {isBatchMode 
                    ? 'Downloading All Videos...' 
                    : 'Downloading...'}
                </span>
              </>
            ) : (
              <>
                <Download className="w-5 h-5" />
                <span>
                  {isBatchMode 
                    ? `Download All ${batchCount} Videos as ZIP` 
                   : 'Download Video'}
                </span>
              </>
            )}
          </button>

          {loading && (
            <div className="mt-6 bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 dark:border-blue-400"></div>
                </div>
                <div className="flex-1">
                  {isBatchMode ? (
                    <>
                      <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
                        Downloading {batchCount} Videos...
                      </h3>
                      <div className="space-y-2 text-sm text-blue-800 dark:text-blue-400">
                        <p>⏳ <strong>Please wait</strong> - The server is downloading all {batchCount} videos and creating a ZIP file</p>
                        <p>📦 All videos will be packaged in a single ZIP file for easy download</p>
                        <p>⏱️ <strong>Estimated time:</strong> {batchCount} × 2-5 minutes = {batchCount * 2}-{batchCount * 5} minutes for HD quality</p>
                        <p>✅ Your ZIP download will start automatically when ready</p>
                        <p className="text-blue-700 dark:text-blue-500 italic mt-3">
                          <strong>Note:</strong> Do not close or refresh this page
                        </p>
                      </div>
                    </>
                  ) : (
                    <>
                      <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
                        Downloading Video...
                      </h3>
                      <div className="space-y-2 text-sm text-blue-800 dark:text-blue-400">
                        <p>⏳ <strong>Please wait</strong> - The server is downloading and processing your video</p>
                        <p>📥 Large files (HD/4K) may take <strong>2-10 minutes</strong> depending on size and quality</p>
                        <p>✅ Your download will start automatically when ready</p>
                        <p className="text-blue-700 dark:text-blue-500 italic mt-3">
                          <strong>Note:</strong> Do not close or refresh this page
                        </p>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Info Box */}
        <div className="bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <div className="space-y-2">
            {isBatchMode ? (
              <>
                <p className="text-sm text-green-800 dark:text-green-400">
                  <strong>💡 Batch Download Times (per video):</strong>
                </p>
                <ul className="text-sm text-green-800 dark:text-green-400 space-y-1 ml-4">
                  <li>• Audio only: ~1 minute × {batchCount} = ~{batchCount} minutes total</li>
                  <li>• 360p-480p: ~2 minutes × {batchCount} = ~{batchCount * 2} minutes total</li>
                  <li>• 720p-1080p: ~4 minutes × {batchCount} = ~{batchCount * 4} minutes total</li>
                  <li>• 2K-4K: ~8 minutes × {batchCount} = ~{batchCount * 8} minutes total</li>
                </ul>
                <p className="text-sm text-green-800 dark:text-green-400 mt-2">
                  <strong>Tip:</strong> Lower quality downloads are much faster. All videos will be packaged in a single ZIP file.
                </p>
              </>
            ) : (
              <>
                <p className="text-sm text-green-800 dark:text-green-400">
                  <strong>💡 Download Times:</strong>
                </p>
                <ul className="text-sm text-green-800 dark:text-green-400 space-y-1 ml-4">
                  <li>• Audio only: 30 seconds - 2 minutes</li>
                  <li>• 360p-480p: 1-3 minutes</li>
                  <li>• 720p-1080p: 2-5 minutes</li>
                  <li>• 2K-4K: 5-10 minutes</li>
                </ul>
                <p className="text-sm text-green-800 dark:text-green-400 mt-2">
                  <strong>Tip:</strong> Audio-only downloads are much faster if you only need the sound.
                </p>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
