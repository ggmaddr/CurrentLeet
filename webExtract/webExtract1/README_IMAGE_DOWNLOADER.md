# Google Drive PDF Image Downloader

Two methods to download all images from a Google Drive PDF viewer when you don't have download permission.

**Filters:** Only downloads images with `w=1600` and `webp=true` parameters.

## Method 1: Browser Console Script (Easiest)

**Best for:** Quick download directly in the browser

### Steps:
1. Open the PDF in Google Drive
2. Open DevTools (F12 or Right-click → Inspect)
3. Go to **Network** tab
4. Filter by **"Img"** to see only images
5. **Scroll through at least one page** to load an image with the correct parameters
6. Go to **Console** tab
7. Copy and paste the contents of `download_drive_images.js`
8. Press Enter
9. **Enter the total number of pages** when prompted

The script will:
- Extract the image URL pattern from loaded images
- Generate URLs for pages 1 through the total number of pages
- Download all images with `w=1600` and `webp=true`
- Save them as `page_001.webp`, `page_002.webp`, etc.

**Note:** You only need to load one page - the script will generate URLs for all pages automatically.

---

## Method 2: HAR File Export + Python Script (Most Reliable)

**Best for:** When Method 1 doesn't work, or you want more control

### Steps:

1. **Open the PDF in Google Drive**
2. **Open DevTools** (F12)
3. **Go to Network tab**
4. **Filter by "Img"** to see only images
5. **Scroll through at least one page** to load an image with `w=1600` and `webp=true`
6. **Export HAR file:**
   - Right-click anywhere in the Network tab
   - Select **"Save all as HAR with content"**
   - Save the file (e.g., `network_log.har`)

7. **Run the Python script:**
   ```bash
   python download_drive_images_har.py network_log.har 33
   ```
   
   Replace `33` with the total number of pages in your PDF.
   
   Or specify a custom output directory:
   ```bash
   python download_drive_images_har.py network_log.har 33 my_images
   ```

The script will:
- Parse the HAR file to find one sample image with `w=1600` and `webp=true`
- Extract the URL pattern and parameters
- Generate URLs for pages 1 through the total number of pages
- Download all images with proper page numbers
- Save them as `page_001.webp`, `page_002.webp`, etc.

### Requirements:
```bash
pip install requests
```

---

## Troubleshooting

### Method 1 doesn't find images:
- Make sure you've scrolled through at least one page
- Check that the images in Network tab have `w=1600` and `webp=true` parameters
- Try refreshing and scrolling again
- Use Method 2 instead (more reliable)

### Method 2: "No images found in HAR file"
- Make sure you filtered by "Img" in Network tab
- Make sure you scrolled through at least one page before exporting
- Check that the images have `w=1600` and `webp=true` in the URL
- Make sure you selected "Save all as HAR **with content**" (not just "Save all as HAR")

### Images fail to download:
- Some URLs may expire. Try:
  1. Keep the PDF tab open
  2. Export HAR again
  3. Run the script immediately

### Getting 403 Forbidden errors:
- The image URLs may require authentication cookies
- Try copying the HAR file and running the script while logged into Google Drive
- The HAR file should contain the necessary cookies/headers

---

## Alternative: Manual HAR Export Method

If you prefer a more manual approach:

1. Export HAR file as described above
2. Open HAR file in a text editor
3. Search for `"url":` entries containing `img?id=`
4. Copy all image URLs
5. Use a download manager or browser extension to download them

---

## Notes

- **Only downloads images with `w=1600` and `webp=true`** - these are the high-quality WebP images
- Images are saved in `.webp` format
- Page numbers are generated sequentially (1, 2, 3, ...) based on the total page count you provide
- Google Drive uses 0-indexed pages in URLs (page=0, page=1, etc.), but files are saved as 1-indexed (page_001, page_002, etc.)
- All images are saved with zero-padded numbers (001, 002, etc.) for proper sorting
- You only need to load one page - the scripts extract the URL pattern and generate all page URLs automatically

