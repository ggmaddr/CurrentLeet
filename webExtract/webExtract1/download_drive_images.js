// Google Drive PDF Image Downloader
// Instructions:
// 1. Open the PDF in Google Drive
// 2. Open DevTools (F12) and go to Network tab
// 3. Filter by "Img" to see only images
// 4. Scroll through the PDF to load at least one page
// 5. Open Console tab in DevTools
// 6. Paste this script and press Enter
// 7. Enter the total number of pages when prompted

(async function downloadAllImages() {
    console.log('Starting image download...');
    
    // Get all network requests from Performance API
    const performanceEntries = performance.getEntriesByType('resource');
    
    // Find images with w=1600 and webp=true
    const imageEntries = performanceEntries.filter(entry => {
        const url = entry.name;
        return url.includes('img?id=') && 
               url.includes('w=1600') && 
               url.includes('webp=true') &&
               (url.includes('drive.google.com') || url.includes('viewerng'));
    });
    
    console.log(`Found ${imageEntries.length} matching image requests (w=1600, webp=true)`);
    
    if (imageEntries.length === 0) {
        console.log('No matching images found. Make sure:');
        console.log('1. You have scrolled through at least one page');
        console.log('2. The images have w=1600 and webp=true in the URL');
        return;
    }
    
    // Get the first image URL to extract base parameters
    const sampleUrl = imageEntries[0].name;
    console.log('Sample URL:', sampleUrl);
    
    // Parse the URL to extract base parameters
    const urlObj = new URL(sampleUrl);
    const baseUrl = `${urlObj.origin}${urlObj.pathname}`;
    const params = new URLSearchParams(urlObj.search);
    
    // Extract key parameters (keep id, authuser, dsmi, etc.)
    const id = params.get('id');
    const authuser = params.get('authuser') || '0';
    const dsmi = params.get('dsmi') || '';
    const auditContext = params.get('auditContext') || 'forDisplay';
    const skiphighlight = params.get('skiphighlight') || 'true';
    
    // Get total number of pages
    const totalPages = parseInt(prompt('Enter the total number of pages in the PDF:') || '0');
    
    if (!totalPages || totalPages <= 0) {
        console.log('Invalid page count. Aborting.');
        return;
    }
    
    console.log(`Will download pages 1 to ${totalPages}...\n`);
    
    // Download each page
    for (let page = 2; page <= totalPages; page++) {
        try {
            // Construct URL with page number, w=1600, webp=true
            const pageParams = new URLSearchParams({
                id: id,
                authuser: authuser,
                dsmi: dsmi,
                auditContext: auditContext,
                page: (page - 1).toString(), // Google Drive uses 0-indexed pages
                skiphighlight: skiphighlight,
                w: '1600',
                webp: 'true'
            });
            
            const imageUrl = `${baseUrl}?${pageParams.toString()}`;
            
            // Fetch the image
            const response = await fetch(imageUrl);
            
            if (!response.ok) {
                console.log(`[${page}/${totalPages}] Page ${page}: ✗ (Status: ${response.status})`);
                continue;
            }
            
            const blob = await response.blob();
            
            // Create download link
            const downloadUrl = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `page_${String(page).padStart(3, '0')}.webp`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            // Clean up
            URL.revokeObjectURL(downloadUrl);
            
            console.log(`[${page}/${totalPages}] Page ${page}: ✓`);
            
            // Small delay to avoid overwhelming the browser
            await new Promise(resolve => setTimeout(resolve, 200));
            
        } catch (error) {
            console.log(`[${page}/${totalPages}] Page ${page}: ✗ Error: ${error.message}`);
        }
    }
    
    console.log('\nDownload complete!');
})();

