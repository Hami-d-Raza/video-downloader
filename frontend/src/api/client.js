import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Analyze a video URL
 * @param {string} url - Video URL to analyze
 * @returns {Promise} Video metadata
 */
export const analyzeVideo = async (url) => {
  try {
    const response = await api.post('/api/analyze', { url });
    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: 'Failed to analyze video' };
  }
};

/**
 * Download a video
 * @param {string} url - Video URL
 * @param {string} formatId - Format ID to download
 * @param {boolean} audioOnly - Download audio only
 * @returns {Promise} Download information
 */
export const downloadVideo = async (url, formatId = null, audioOnly = false) => {
  try {
    const response = await api.post('/api/download', {
      url,
      format_id: formatId,
      audio_only: audioOnly,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: 'Failed to download video' };
  }
};

/**
 * Get file download URL
 * @param {string} filename - Filename to download
 * @returns {string} Download URL
 */
export const getFileUrl = (filename) => {
  return `${API_BASE_URL}/api/file/${filename}`;
};

/**
 * Check API health
 * @returns {Promise} API status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;
