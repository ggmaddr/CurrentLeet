// Google Drive Video Downloader
// Instructions:
// OPTION 1 (Before video loads - intercepts requests):
// 1. Open DevTools (F12) → Console tab FIRST
// 2. Paste this script and press Enter
// 3. Then open the video in Google Drive and play it
//
// OPTION 2 (After video loads - uses Performance API):
// 1. Open the video in Google Drive
// 2. Play the video and let it load
// 3. Open DevTools (F12) → Console tab
// 4. Paste this script and press Enter
//
// If this doesn't work, use the Python HAR script instead:
// python download_drive_video_har.py <har_file>

// Intercept fetch and XMLHttpRequest to capture URLs
let interceptedUrls = { video: null, audio: null };

(function setupInterceptor() {
    // Intercept fetch
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        const url = args[0];
        if (typeof url === 'string' && url.includes('videoplayback')) {
            if (url.includes('mime=video') && !interceptedUrls.video) {
                interceptedUrls.video = url;
            }
            if (url.includes('mime=audio') && !interceptedUrls.audio) {
                interceptedUrls.audio = url;
            }
        }
        return originalFetch.apply(this, args);
    };
    
    // Intercept XMLHttpRequest
    const originalOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url, ...rest) {
        if (typeof url === 'string' && url.includes('videoplayback')) {
            if (url.includes('mime=video') && !interceptedUrls.video) {
                interceptedUrls.video = url;
            }
            if (url.includes('mime=audio') && !interceptedUrls.audio) {
                interceptedUrls.audio = url;
            }
        }
        return originalOpen.apply(this, [method, url, ...rest]);
    };
    
    console.log('✅ Network interceptor installed. Now play the video.');
})();

(function extractVideoUrls() {
    console.log('\nExtracting video and audio URLs...\n');
    
    // Get all network requests from Performance API
    const performanceEntries = performance.getEntriesByType('resource');
    
    console.log(`Total performance entries: ${performanceEntries.length}`);
    
    // Debug: Show all URLs containing 'mime'
    const mimeEntries = performanceEntries.filter(e => e.name.includes('mime='));
    console.log(`Entries with 'mime=': ${mimeEntries.length}`);
    if (mimeEntries.length > 0) {
        console.log('Sample entries with mime:');
        mimeEntries.slice(-5).forEach((e, i) => {
            const mimeMatch = e.name.match(/mime=([^&]+)/);
            console.log(`  ${i + 1}. ${mimeMatch ? mimeMatch[1] : 'unknown'}`);
        });
    }
    
    let videoUrl = null;
    let audioUrl = null;
    
    // Find the last entry with &mime=video and &mime=audio
    // Try both 'mime=video' and 'mime=video/mp4' patterns
    for (let i = performanceEntries.length - 1; i >= 0; i--) {
        const url = performanceEntries[i].name;
        
        // Get the last video URL (check for both patterns)
        if ((url.includes('&mime=video') || url.includes('mime=video')) && !videoUrl) {
            videoUrl = url;
        }
        
        // Get the last audio URL
        if ((url.includes('&mime=audio') || url.includes('mime=audio')) && !audioUrl) {
            audioUrl = url;
        }
        
        // Stop if we found both
        if (videoUrl && audioUrl) {
            break;
        }
    }
    
    // Check intercepted URLs first (more reliable)
    if (interceptedUrls.video) {
        videoUrl = interceptedUrls.video;
        console.log('Found video URL via interceptor');
    }
    if (interceptedUrls.audio) {
        audioUrl = interceptedUrls.audio;
        console.log('Found audio URL via interceptor');
    }
    
    // If not found, try alternative: check all entries for videoplayback
    if (!videoUrl || !audioUrl) {
        console.log('\nTrying alternative method: searching all entries...');
        const allEntries = performance.getEntries();
        
        for (let i = allEntries.length - 1; i >= 0; i--) {
            const entry = allEntries[i];
            const url = entry.name || entry.initiatorType || '';
            
            if ((url.includes('mime=video') || url.includes('mime=video/mp4')) && !videoUrl) {
                videoUrl = url;
            }
            
            if ((url.includes('mime=audio') || url.includes('mime=audio/mp4')) && !audioUrl) {
                audioUrl = url;
            }
            
            if (videoUrl && audioUrl) break;
        }
    }
    
    // Function to remove everything from &range onwards
    function cleanUrl(url) {
        if (!url) return null;
        const rangeIndex = url.indexOf('&range');
        if (rangeIndex !== -1) {
            return url.substring(0, rangeIndex);
        }
        return url;
    }
    
    // Clean both URLs
    const cleanedVideoUrl = cleanUrl(videoUrl);
    const cleanedAudioUrl = cleanUrl(audioUrl);
    
    // Print the 2 cleaned URLs
    console.log('\n' + '='.repeat(80));
    
    if (cleanedVideoUrl) {
        console.log('VIDEO URL:');
        console.log(cleanedVideoUrl);
    } else {
        console.log('VIDEO URL: Not found');
        console.log('\nTo find manually:');
        console.log('1. Go to Network tab');
        console.log('2. Filter by "videoplayback" or search for "mime=video"');
        console.log('3. Find the latest request with "mime=video"');
        console.log('4. Copy the Request URL');
        console.log('5. Remove everything from "&range" onwards');
    }
    
    if (cleanedAudioUrl) {
        console.log('\nAUDIO URL:');
        console.log(cleanedAudioUrl);
    } else {
        console.log('\nAUDIO URL: Not found');
        console.log('\nTo find manually:');
        console.log('1. Go to Network tab');
        console.log('2. Filter by "videoplayback" or search for "mime=audio"');
        console.log('3. Find the latest request with "mime=audio"');
        console.log('4. Copy the Request URL');
        console.log('5. Remove everything from "&range" onwards');
    }
    
    console.log('\n' + '='.repeat(80));
    
    if (!cleanedVideoUrl || !cleanedAudioUrl) {
        console.log('\n⚠️  Performance API may not capture all requests.');
        console.log('Alternative: Export HAR file from Network tab and use a Python script.');
    }
    
    // Return URLs for programmatic use
    return {
        video: cleanedVideoUrl,
        audio: cleanedAudioUrl
    };
})();

