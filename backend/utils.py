"""
Utility functions for video downloader
"""

import os
import re
import time
from typing import Optional
from collections import defaultdict
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def validate_url(url: str) -> bool:
    """
    Validate if the URL is properly formatted
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))


def detect_platform(url: str) -> Optional[str]:
    """
    Detect the platform from the URL
    
    Args:
        url: Video URL
        
    Returns:
        Platform name or None if unsupported
    """
    url_lower = url.lower()
    
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'YouTube'
    elif 'facebook.com' in url_lower or 'fb.watch' in url_lower:
        return 'Facebook'
    elif 'instagram.com' in url_lower:
        return 'Instagram'
    elif 'tiktok.com' in url_lower:
        return 'TikTok'
    
    return None


def cleanup_old_files(directory: str, hours: float = 1) -> int:
    """
    Delete files older than specified hours
    
    Args:
        directory: Directory to clean
        hours: Age threshold in hours
        
    Returns:
        Number of files deleted
    """
    if not os.path.exists(directory):
        return 0
    
    deleted_count = 0
    current_time = time.time()
    age_threshold = hours * 3600  # Convert to seconds
    
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > age_threshold:
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                        logger.info(f"Deleted old file: {filename}")
                    except Exception as e:
                        logger.error(f"Error deleting {filename}: {e}")
    
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
    
    return deleted_count


class RateLimiter:
    """Simple rate limiter to prevent abuse"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum requests allowed in the time window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def check_rate_limit(self, identifier: str) -> bool:
        """
        Check if request is within rate limit
        
        Args:
            identifier: Unique identifier (e.g., IP address or URL)
            
        Returns:
            True if within limit, False if exceeded
        """
        current_time = time.time()
        
        # Clean old requests
        self.requests[identifier] = [
            timestamp for timestamp in self.requests[identifier]
            if current_time - timestamp < self.window_seconds
        ]
        
        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for: {identifier}")
            return False
        
        # Add new request
        self.requests[identifier].append(current_time)
        return True
    
    def cleanup_old_entries(self):
        """Cleanup old entries to prevent memory bloat"""
        current_time = time.time()
        
        for identifier in list(self.requests.keys()):
            self.requests[identifier] = [
                timestamp for timestamp in self.requests[identifier]
                if current_time - timestamp < self.window_seconds
            ]
            
            # Remove empty entries
            if not self.requests[identifier]:
                del self.requests[identifier]


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=20, window_seconds=60)


def format_filesize(bytes_size: int) -> str:
    """
    Format filesize to human-readable string
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    if bytes_size >= 1024 ** 3:
        return f"{bytes_size / (1024 ** 3):.2f} GB"
    elif bytes_size >= 1024 ** 2:
        return f"{bytes_size / (1024 ** 2):.2f} MB"
    elif bytes_size >= 1024:
        return f"{bytes_size / 1024:.2f} KB"
    else:
        return f"{bytes_size} bytes"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 200:
        name = name[:200]
    
    return name + ext
