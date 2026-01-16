#!/usr/bin/env python3
"""
Google Drive PDF Image Downloader (HAR Method)
This script parses a HAR file exported from Chrome DevTools and downloads all images.

Instructions:
1. Open the PDF in Google Drive
2. Open DevTools (F12) and go to Network tab
3. Filter by "Img" to see only images
4. Scroll through at least one page of the PDF
5. Right-click in the Network tab → "Save all as HAR with content"
6. Save the HAR file
7. Run this script: python download_drive_images_har.py <path_to_har_file> [total_pages]
"""

import json
import sys
import os
import re
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from pathlib import Path

def extract_sample_image_from_har(har_file_path):
    """Extract one sample image URL with w=1600 and webp=true from HAR file."""
    with open(har_file_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    # Find images with w=1600 and webp=true
    for entry in har_data.get('log', {}).get('entries', []):
        request = entry.get('request', {})
        response = entry.get('response', {})
        
        url = request.get('url', '')
        mime_type = response.get('content', {}).get('mimeType', '')
        
        # Check if it's an image request with w=1600 and webp=true
        if ('img?id=' in url or 'viewerng' in url) and \
           'image' in mime_type.lower() and \
           'w=1600' in url and \
           'webp=true' in url:
            
            headers = {h['name']: h['value'] for h in request.get('headers', [])}
            return url, headers
    
    return None, None

def parse_url_and_generate_pages(sample_url, total_pages):
    """Parse sample URL and generate URLs for all pages."""
    parsed = urlparse(sample_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    params = parse_qs(parsed.query)
    
    # Extract key parameters
    image_id = params.get('id', [''])[0]
    authuser = params.get('authuser', ['0'])[0]
    dsmi = params.get('dsmi', [''])[0]
    audit_context = params.get('auditContext', ['forDisplay'])[0]
    skiphighlight = params.get('skiphighlight', ['true'])[0]
    
    # Generate URLs for all pages
    urls = []
    for page in range(total_pages):
        page_params = {
            'id': image_id,
            'authuser': authuser,
            'dsmi': dsmi,
            'auditContext': audit_context,
            'page': str(page),  # Google Drive uses 0-indexed pages
            'skiphighlight': skiphighlight,
            'w': '1600',
            'webp': 'true'
        }
        url = f"{base_url}?{urlencode(page_params)}"
        urls.append((page + 1, url))  # Store 1-indexed page number for filename
    
    return urls

def download_image(url, headers, output_path):
    """Download an image from URL."""
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_drive_images_har.py <har_file_path> <total_pages> [output_directory]")
        print("\nExample: python download_drive_images_har.py network.har 33")
        print("\nTo export HAR file:")
        print("1. Open DevTools → Network tab")
        print("2. Filter by 'Img'")
        print("3. Scroll through at least one page")
        print("4. Right-click → 'Save all as HAR with content'")
        sys.exit(1)
    
    har_file = sys.argv[1]
    
    # Get total pages
    try:
        total_pages = int(sys.argv[2])
    except (IndexError, ValueError):
        print("Error: Please provide the total number of pages as the second argument")
        print("Usage: python download_drive_images_har.py <har_file_path> <total_pages> [output_directory]")
        sys.exit(1)
    
    output_dir = sys.argv[3] if len(sys.argv) > 3 else 'downloaded_images'
    
    if not os.path.exists(har_file):
        print(f"Error: HAR file not found: {har_file}")
        sys.exit(1)
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"Parsing HAR file: {har_file}")
    sample_url, sample_headers = extract_sample_image_from_har(har_file)
    
    if not sample_url:
        print("No matching images found in HAR file (w=1600, webp=true).")
        print("Make sure you:")
        print("1. Filtered by 'Img' in Network tab")
        print("2. Scrolled through at least one page")
        print("3. The images have w=1600 and webp=true parameters")
        print("4. Exported HAR with 'Save all as HAR with content'")
        sys.exit(1)
    
    print(f"Found sample image URL")
    print(f"Generating URLs for pages 1 to {total_pages}...\n")
    
    # Generate URLs for all pages
    image_urls = parse_url_and_generate_pages(sample_url, total_pages)
    
    print(f"Will download {len(image_urls)} images")
    print(f"Output directory: {output_dir}\n")
    
    # Download all images
    success_count = 0
    for page_num, url in image_urls:
        filename = f"page_{page_num:03d}.webp"
        output_path = os.path.join(output_dir, filename)
        
        print(f"[{page_num}/{total_pages}] Downloading {filename}...", end=' ')
        
        if download_image(url, sample_headers, output_path):
            print("✓")
            success_count += 1
        else:
            print("✗")
    
    print(f"\nDownload complete! {success_count}/{len(image_urls)} images downloaded.")
    print(f"Images saved to: {os.path.abspath(output_dir)}")

if __name__ == '__main__':
    main()

