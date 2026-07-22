/**
 * Terminal Archives - Main Script
 * Phase 1 Secure Core – XSS hardening
 */
document.addEventListener('DOMContentLoaded', function () {
    const output = document.getElementById('output');
    const searchModal = document.getElementById('search-modal');
    const searchInput = document.getElementById('search-input');
    const mobileSearchInput = document.getElementById('mobile-search-input');

    function escapeHTML(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function addLine(text, className = '') { 
        const line = document.createElement('div'); 
        line.innerHTML = text; 
        line.className = `line ${className}`; 
        output.appendChild(line); 
        window.scrollTo(0, document.body.scrollHeight); 
    }

    function addText(text, className='') {
        const line = document.createElement('div');
        line.textContent = text;
        line.className = `line ${className}`;
        output.appendChild(line);
        window.scrollTo(0, document.body.scrollHeight);
    }
    
    function sleep(ms) { 
        return new Promise(resolve => setTimeout(resolve, ms)); 
    }
    
    async function showProgressBar(text, duration) { 
        const line = document.createElement('div'); 
        line.className = 'line progress-bar-container'; 
        line.innerHTML = `<span>${escapeHTML(text)}</span><div class="progress-bar-wrapper"><div class="progress-bar"></div></div>`; 
        output.appendChild(line); 
        await sleep(duration); 
        line.remove(); 
    }
    
    async function fetchDeviceInfo() { 
        addLine('Device Information:'); 
        const cores = navigator.hardwareConcurrency || 'N/A'; 
        addLine(`  - Logical CPU Cores: <span class="highlight">${escapeHTML(cores)}</span>`); 
        const memory = navigator.deviceMemory ? `${navigator.deviceMemory} GB (browser approx.)` : 'N/A'; 
        addLine(`  - Device Memory (RAM): <span class="highlight">${escapeHTML(memory)}</span>`); 
        if (navigator.storage && navigator.storage.estimate) { 
            const estimate = await navigator.storage.estimate(); 
            const usageMB = (estimate.usage / 1024 / 1024).toFixed(2); 
            const quotaMB = (estimate.quota / 1024 / 1024).toFixed(2); 
            addLine(`  - Browser Storage Quota: <span class="highlight">${escapeHTML(usageMB)} MB used / ${escapeHTML(quotaMB)} MB total</span>`); 
        } else { 
            addLine('  - Browser Storage: API not supported.'); 
        } 
        addLine('// Note: Browser security prevents access to total disk space or system RAM.', 'comment'); 
    }

    function handleAdminShortcut() {
        addLine('// Redirecting to Admin Login page...', 'comment');
        setTimeout(() => { window.location.href = '/login'; }, 1000);
    }

    async function performSearch(query) {
        if (query.trim().toLowerCase() === 'upload') { 
            handleAdminShortcut(); 
            return; 
        }
        // C3 – escape query before innerHTML
        const qSafe = escapeHTML(query);
        addLine(`<span class="prompt">user@archives:~$</span> <span class="command">search --query="${qSafe}"</span>`);
        await showProgressBar('Searching database...', 1000);
        
        try {
            const response = await fetch(`/api/papers?q=${encodeURIComponent(query)}&limit=100`);
            const results = await response.json();
            
            if (results.length > 0) {
                addLine(`Found <span class="highlight">${results.length}</span> result(s):`);
                results.forEach(paper => {
                    // Build DOM safely
                    const wrapper = document.createElement('div');
                    wrapper.className = 'search-result';
                    const year = document.createElement('span');
                    year.textContent = `[${paper.exam_year || ''}] `;
                    const a = document.createElement('a');
                    a.href = paper.url;
                    a.target = '_blank';
                    a.rel = 'noopener noreferrer';
                    // original_name is server-escaped already, still use textContent
                    a.textContent = paper.original_name || `${paper.subject} ${paper.exam_type} ${paper.exam_year}`;
                    wrapper.appendChild(year);
                    wrapper.appendChild(a);
                    const line = document.createElement('div');
                    line.className = 'line';
                    line.appendChild(wrapper);
                    output.appendChild(line);
                });
                window.scrollTo(0, document.body.scrollHeight);
            } else { 
                addLine('No results found for your query.'); 
            }
        } catch (error) { 
            addLine('// Error connecting to the search API.', 'comment'); 
        }
        
        addLine(`<br/><span class="desktop-only">// Press Ctrl + K to search again.</span>`);
    }

    async function start() {
        addLine('// Welcome to the Terminal Archives.', 'comment'); 
        await sleep(500);
        await showProgressBar('Connecting to archives...', 1500);
        
        try {
            const response = await fetch('/api/papers?limit=1');
            if (response.ok) {
                // we can't know total without count endpoint; show at least connected
                addLine(`// Connected. Archive online.`);
            } else {
                addLine('// Connection to archives failed (Server Error).', 'comment');
            }
        } catch (error) { 
            addLine('// Connection to archives failed.', 'comment'); 
            console.error('Fetch error:', error); 
        }
        
        await sleep(500);
        await showProgressBar('Initializing system...', 1000);
        addLine('<span class="prompt">system@archives:~$</span> <span class="command">fetch --device-info</span>');
        await fetchDeviceInfo();
        await sleep(500);
        addLine('<span class="prompt">system@archives:~$</span> <span class="command">ready</span>');
        addLine(`System ready. <span class="desktop-only">Press Ctrl + K to search the database.</span>`);
    }

    window.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') { 
            e.preventDefault(); 
            if(searchModal){
                searchModal.classList.remove('hidden'); 
                if(searchInput){ searchInput.focus(); searchInput.value = ''; }
            }
        }
        if (e.key === 'Escape') { 
            if (searchModal && !searchModal.classList.contains('hidden')) { 
                searchModal.classList.add('hidden'); 
            } 
        }
    });
    
    if(searchInput){
        searchInput.addEventListener('keydown', (e) => { 
            if (e.key === 'Enter') { 
                e.preventDefault(); 
                if(searchModal) searchModal.classList.add('hidden'); 
                performSearch(searchInput.value); 
            } 
        });
    }
    
    if(mobileSearchInput){
        mobileSearchInput.addEventListener('keydown', (e) => { 
            if (e.key === 'Enter') { 
                performSearch(mobileSearchInput.value); 
                mobileSearchInput.value = ''; 
                mobileSearchInput.blur(); 
            } 
        });
    }

    if(searchModal){
        searchModal.addEventListener('click', (e) => {
            if (e.target === searchModal) {
                searchModal.classList.add('hidden');
            }
        });
    }

    start();
});
