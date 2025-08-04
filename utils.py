"""Utility functions for the Telegram automation system."""

import re
from typing import Optional
from urllib.parse import urlparse

class URLValidator:
    """URL validation utilities for Instagram and YouTube."""
    
    # Instagram URL patterns
    INSTAGRAM_PATTERNS = [
        r'https?://(?:www\.)?instagram\.com/p/[A-Za-z0-9_-]+/?(?:\?.*)?',
        r'https?://(?:www\.)?instagram\.com/reel/[A-Za-z0-9_-]+/?(?:\?.*)?',
        r'https?://(?:www\.)?instagram\.com/reels/[A-Za-z0-9_-]+/?(?:\?.*)?',
        r'https?://(?:www\.)?instagram\.com/tv/[A-Za-z0-9_-]+/?(?:\?.*)?',
        r'https?://(?:www\.)?instagram\.com/stories/[A-Za-z0-9_.]+/\d+/?(?:\?.*)?',
    ]
    
    # YouTube URL patterns
    YOUTUBE_PATTERNS = [
        r'https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]+',
        r'https?://(?:www\.)?youtu\.be/[A-Za-z0-9_-]+',
        r'https?://(?:www\.)?youtube\.com/shorts/[A-Za-z0-9_-]+',
        r'https?://m\.youtube\.com/watch\?v=[A-Za-z0-9_-]+',
    ]
    
    # TikTok URL patterns
    TIKTOK_PATTERNS = [
        r'https?://(?:www\.)?tiktok\.com/@[A-Za-z0-9_.]+/video/\d+',
        r'https?://(?:vm|vt)\.tiktok\.com/[A-Za-z0-9]+/?',
        r'https?://(?:www\.)?tiktok\.com/t/[A-Za-z0-9]+/?',
        r'https?://m\.tiktok\.com/v/\d+',
    ]
    
    @classmethod
    def is_instagram_url(cls, url: str) -> bool:
        """
        Check if the URL is a valid Instagram URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid Instagram URL, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        # Clean the URL
        url = url.strip()
        
        # Check against patterns
        for pattern in cls.INSTAGRAM_PATTERNS:
            if re.match(pattern, url, re.IGNORECASE):
                return True
        
        return False
    
    @classmethod
    def is_youtube_url(cls, url: str) -> bool:
        """
        Check if the URL is a valid YouTube URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid YouTube URL, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        # Clean the URL
        url = url.strip()
        
        # Check against patterns
        for pattern in cls.YOUTUBE_PATTERNS:
            if re.match(pattern, url, re.IGNORECASE):
                return True
        
        return False
    
    @classmethod
    def is_tiktok_url(cls, url: str) -> bool:
        """
        Check if the URL is a valid TikTok URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid TikTok URL, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        # Clean the URL
        url = url.strip()
        
        # Check against patterns
        for pattern in cls.TIKTOK_PATTERNS:
            if re.match(pattern, url, re.IGNORECASE):
                return True
        
        return False
    
    @classmethod
    def is_valid_url(cls, url: str) -> bool:
        """
        Check if the URL is a valid Instagram, YouTube or TikTok URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid URL, False otherwise
        """
        return cls.is_instagram_url(url) or cls.is_youtube_url(url) or cls.is_tiktok_url(url)
    
    @classmethod
    def get_url_type(cls, url: str) -> Optional[str]:
        """
        Get the type of URL (instagram, youtube or tiktok).
        
        Args:
            url: URL to check
            
        Returns:
            'instagram', 'youtube', 'tiktok' or None if invalid
        """
        if cls.is_instagram_url(url):
            return 'instagram'
        elif cls.is_youtube_url(url):
            return 'youtube'
        elif cls.is_tiktok_url(url):
            return 'tiktok'
        return None
    
    @classmethod
    def normalize_url(cls, url: str) -> Optional[str]:
        """
        Normalize URL by removing tracking parameters and fragments.
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL or None if invalid
        """
        if not cls.is_valid_url(url):
            return None
        
        try:
            url = url.strip()
            
            # For YouTube URLs, keep the necessary query parameters (v parameter)
            if cls.is_youtube_url(url):
                parsed = urlparse(url)
                if 'youtube.com' in parsed.netloc and '/watch' in parsed.path:
                    # Extract video ID from query parameters
                    from urllib.parse import parse_qs
                    query_params = parse_qs(parsed.query)
                    if 'v' in query_params:
                        video_id = query_params['v'][0]
                        return f"https://www.youtube.com/watch?v={video_id}"
                elif 'youtu.be' in parsed.netloc:
                    # Extract video ID from path
                    video_id = parsed.path.lstrip('/')
                    return f"https://www.youtube.com/watch?v={video_id}"
                # For shorts and other formats, just normalize the domain and path
                return f"https://www.youtube.com{parsed.path}"
            
            # For TikTok URLs, remove query parameters and fragments
            elif cls.is_tiktok_url(url):
                parsed = urlparse(url)
                normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                # Remove trailing slash
                normalized = normalized.rstrip('/')
                return normalized
            
            # For Instagram URLs, remove query parameters and fragments
            else:
                parsed = urlparse(url)
                normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                # Remove trailing slash
                normalized = normalized.rstrip('/')
                return normalized
                
        except Exception:
            return None
    
    @classmethod
    def extract_urls_from_text(cls, text: str) -> list[str]:
        """
        Extract all valid URLs from text.
        
        Args:
            text: Text to search for URLs
            
        Returns:
            List of found URLs
        """
        if not text:
            return []
        
        # Combine all patterns
        all_patterns = cls.INSTAGRAM_PATTERNS + cls.YOUTUBE_PATTERNS + cls.TIKTOK_PATTERNS
        
        urls = []
        for pattern in all_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            urls.extend(matches)
        
        # Normalize and deduplicate
        normalized_urls = []
        for url in urls:
            normalized = cls.normalize_url(url)
            if normalized and normalized not in normalized_urls:
                normalized_urls.append(normalized)
        
        return normalized_urls


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters for Windows/Unix
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"
    
    return filename
