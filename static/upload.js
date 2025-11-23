/**
 * Terminal Archives - Upload Script
 * ==================================
 * Handles drag-and-drop file upload, form validation, and batch uploads.
 * Manages the admin dashboard upload functionality.
 * 
 * Features:
 * - Drag and drop multiple PDF files
 * - Dynamic form card generation for each file
 * - Real-time validation
 * - Batch upload with progress tracking
 * - Keyboard navigation between form cards
 * - CSRF token protection
 * 
 * Author: Alvido
 * Last Updated: 2025
 */

document.addEventListener('DOMContentLoaded', function () {
    // DOM element references
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const formsWrapper = document.getElementById('forms-wrapper');
    const uploadAllBtn = document.getElementById('upload-all-btn');

    // Get the CSRF token from meta tag for secure form submission
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Map to track added files and prevent duplicates
    // Key: "filename-filesize", Value: {file, card, uploaded}
    let addedFiles = new Map();
    // ========== Event Listeners ==========
    
    /**
     * Dragover event - prevent default and show visual feedback
     */
    dropZone.addEventListener('dragover', (e) => { 
        e.preventDefault(); 
        dropZone.classList.add('drag-over'); 
    });
    
    /**
     * Dragleave event - remove visual feedback
     */
    dropZone.addEventListener('dragleave', () => { 
        dropZone.classList.remove('drag-over'); 
    });
    
    /**
     * Drop event - handle dropped files
     */
    dropZone.addEventListener('drop', (e) => { 
        e.preventDefault(); 
        dropZone.classList.remove('drag-over'); 
        handleFiles(e.dataTransfer.files); 
    });
    
    /**
     * File input change event - handle selected files
     */
    fileInput.addEventListener('change', (e) => { 
        handleFiles(e.target.files); 
    });

    /**
     * Process and validate dropped/selected files
     * @param {FileList} files - The files to process
     */
    function handleFiles(files) {
        for (const file of files) {
            // Create unique identifier for duplicate detection
            const fileIdentifier = `${file.name}-${file.size}`;
            
            // Validate file type (PDF only)
            if (file.type !== 'application/pdf') { 
                alert(`'${file.name}' is not a PDF and will be ignored.`); 
                continue; 
            }
            
            // Check for duplicates
            if (addedFiles.has(fileIdentifier)) { 
                alert(`'${file.name}' has already been added.`); 
                continue; 
            }
            
            // Create form card for this file
            const card = createFormCard(file);
            formsWrapper.appendChild(card);
            addedFiles.set(fileIdentifier, { file: file, card: card, uploaded: false });
        }
    }

    /**
     * Create a form card for a single file
     * @param {File} file - The file to create a form for
     * @returns {HTMLElement} The created form card element
     */
    function createFormCard(file) {
        const card = document.createElement('div');
        card.className = 'form-card';
        
        // Generate comprehensive form HTML with all required and optional fields
        card.innerHTML = `
            <h3 title="${file.name}">${file.name}</h3>
            <div class="status-indicator">Pending</div>

            <label>Your Name:</label> <input type="text" name="admin_name" placeholder="e.g., Alvido" required>

            <label>Class:</label> <select name="class" required> <option value="" disabled selected>Select a Class</option> <option value="BA">BA</option> <option value="BSc">BSc</option> <option value="BA/BSc">BA/BSc</option> <option value="BSc Hons">BSc Hons</option> <option value="BSc/BSc Hons">BSc/BSc Hons</option> <option value="BBA">BBA</option> <option value="BCA">BCA</option> <option value="MCA">MCA</option> </select>
            <label>Subject:</label> <select name="subject" required> <option value="" disabled selected>Select a Subject</option> <option value="Maths">Maths</option> <option value="Physics">Physics</option> <option value="Chemistry">Chemistry</option> <option value="Hindi">Hindi</option> <option value="English">English</option> <option value="Biology">Biology</option> <option value="Psychology">Psychology</option> <option value="Zoology">Zoology</option> <option value="Computer Science">Computer Science</option> <option value="Political Science">Political Science</option> <option value="Statistics">Statistics</option> <option value="Geography">Geography</option> <option value="Biotechnology">Biotechnology</option> <option value="Microbiology">Microbiology</option> <option value="Environmental Science">Environmental Science</option> <option value="History">History</option> <option value="Economics">Economics</option> </select>
            <label>Semester:</label> <select name="semester" required> <option value="" disabled selected>Select a Semester</option> <option value="I">I (1)</option> <option value="II">II (2)</option> <option value="III">III (3)</option> <option value="IV">IV (4)</option> <option value="V">V (5)</option> <option value="VI">VI (6)</option> <option value="VII">VII (7)</option> <option value="VIII">VIII (8)</option> <option value="IX">IX (9)</option> <option value="X">X (10)</option> <option value="All Semesters">All Semesters</option> </select>
            <label>Exam Year:</label> <input list="years" name="exam_year" placeholder="e.g., 2025" required>
            <label>Exam Type:</label> <select name="exam_type" required> <option value="" disabled selected>Select an Exam Type</option> <option value="Main Semester">Main Semester</option> <option value="CIA">CIA</option> <option value="Half Yearly">Half Yearly</option> <option value="Class Test">Class Test</option> <option value="Yearly">Yearly</option> <option value="Assignments">Assignments</option> <option value="Notes">Notes</option> </select>
            <label>Exam Number (Optional):</label> <input list="paper_counts" name="exam_number" placeholder="e.g., First Paper (1)">
            <label>Paper Code (Optional):</label> <input type="text" name="paper_code" placeholder="Enter paper code">
            <label>Medium:</label> <select name="medium" required> <option value="" disabled selected>Select a Medium</option> <option value="English Medium">English Medium</option> <option value="Hindi Medium">Hindi Medium</option> <option value="Hinglish">Hinglish</option> </select>
            <label>University / College (Optional):</label> <input list="universities" name="university" placeholder="e.g., University of Rajasthan">
            <label>Time (Optional):</label> <input list="times" name="time" placeholder="e.g., 3 hr">
            <label>Max Marks (Optional):</label> <input list="marks" name="max_marks" placeholder="e.g., 100">
        `;
        return card;
    }

    /**
     * Validate that all required fields in a form card are filled
     * @param {HTMLElement} card - The form card to validate
     * @returns {boolean} True if valid, false otherwise
     */
    function validateForm(card) {
        const requiredInputs = card.querySelectorAll('[required]');
        let isValid = true;
        
        // Check if all required fields have values
        for (const input of requiredInputs) { 
            if (!input.value) { 
                isValid = false; 
                break; 
            } 
        }
        
        // Show error indicator if validation fails
        if (!isValid) {
            const statusIndicator = card.querySelector('.status-indicator');
            statusIndicator.textContent = '❌ Missing Info!';
            statusIndicator.style.backgroundColor = 'var(--error-color)';
            card.classList.add('form-error');
        } else {
            card.classList.remove('form-error');
        }
        
        return isValid;
    }

    /**
     * Upload all pending files button click handler
     * Validates and uploads each file sequentially
     */
    uploadAllBtn.addEventListener('click', async () => {
        for (const [identifier, data] of addedFiles.entries()) {
            // Only upload if not already uploaded and validation passes
            if (!data.uploaded && validateForm(data.card)) {
                await uploadFile(data);
            }
        }
    });

    /**
     * Upload a single file with its metadata to the server
     * @param {Object} data - Object containing file, card, and uploaded status
     */
    async function uploadFile(data) {
        const { file, card } = data;
        const statusIndicator = card.querySelector('.status-indicator');
        
        // Update status to "Uploading"
        statusIndicator.textContent = 'Uploading...';
        statusIndicator.style.backgroundColor = '#f0ad4e';

        // Prepare form data with file and all metadata
        const formData = new FormData();
        formData.append('file', file);

        // Collect all input values from the form card
        const inputs = card.querySelectorAll('input, select');
        for (const input of inputs) { 
            formData.append(input.name, input.value); 
        }

        try {
            // Send upload request with CSRF token for security
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });

            if (response.ok) {
                // Upload successful
                statusIndicator.textContent = '✅ Uploaded';
                statusIndicator.style.backgroundColor = '#5cb85c';
                data.uploaded = true;
            } else {
                // Upload failed
                statusIndicator.textContent = '❌ Failed';
                statusIndicator.style.backgroundColor = '#d9534f';
            }
        } catch (error) {
            // Network error
            console.error('Upload error:', error);
            statusIndicator.textContent = '❌ Network Error';
            statusIndicator.style.backgroundColor = '#d9534f';
        }
    }

    /**
     * Keyboard navigation for form cards
     * Left/Right arrow keys scroll between cards
     */
    document.addEventListener('keydown', (e) => {
        // Don't interfere with form input
        if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'SELECT') { 
            return; 
        }
        
        const scrollAmount = 420; // Width of one card plus gap
        
        if (e.key === 'ArrowRight') { 
            formsWrapper.scrollBy({ left: scrollAmount, behavior: 'smooth' }); 
        }
        else if (e.key === 'ArrowLeft') { 
            formsWrapper.scrollBy({ left: -scrollAmount, behavior: 'smooth' }); 
        }
    });
});
