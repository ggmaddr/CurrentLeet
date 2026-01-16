#!/usr/bin/env python3
"""
Google Drive Video URL Extractor (HAR Method)
Extracts video and audio URLs from a HAR file exported from Chrome DevTools.

Instructions:
1. Open the video in Google Drive
2. Open DevTools (F12) → Network tab
3. Play the video and let it load
4. Right-click in Network tab → "Save all as HAR with content"
5. Run: python download_drive_video_har.py <har_file_path>
"""

import json
import sys
import re
from urllib.parse import urlparse, parse_qs

def extract_video_urls_from_har(har_file_path):
    """Extract video and audio URLs from HAR file."""
    with open(har_file_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    video_url = None
    audio_url = None
    
    # Iterate through all entries
    for entry in har_data.get('log', {}).get('entries', []):
        request = entry.get('request', {})
        url = request.get('url', '')
        
        # Check for video URL
        if ('mime=video' in url or 'mime=video/mp4' in url) and not video_url:
            video_url = url
        
        # Check for audio URL
        if ('mime=audio' in url or 'mime=audio/mp4' in url) and not audio_url:
            audio_url = url
    
    return video_url, audio_url

def clean_url(url):
    """Remove everything from &range onwards."""
    if not url:
        return None
    
    range_index = url.find('&range')
    if range_index != -1:
        return url[:range_index]
    return url

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_drive_video_har.py <har_file_path>")
        print("\nTo export HAR file:")
        print("1. Open DevTools → Network tab")
        print("2. Play the video")
        print("3. Right-click → 'Save all as HAR with content'")
        sys.exit(1)
    
    har_file = sys.argv[1]
    
    try:
        video_url, audio_url = extract_video_urls_from_har(har_file)
    except FileNotFoundError:
        print(f"Error: HAR file not found: {har_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid HAR file: {har_file}")
        sys.exit(1)
    
    # Clean URLs
    cleaned_video = clean_url(video_url)
    cleaned_audio = clean_url(audio_url)
    
    # Print results
    print('=' * 80)
    print('CLEANED URLs (ready for download):')
    print('=' * 80)
    
    if cleaned_video:
        print('\nVIDEO URL:')
        print(cleaned_video)
    else:
        print('\nVIDEO URL: Not found')
    
    if cleaned_audio:
        print('\nAUDIO URL:')
        print(cleaned_audio)
    else:
        print('\nAUDIO URL: Not found')
    
    print('\n' + '=' * 80)

if __name__ == '__main__':
    main()

