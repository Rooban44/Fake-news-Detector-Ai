// File upload UI handling ONLY
const fileUploadArea = document.getElementById('fileUploadArea');
const fileInput = document.getElementById('fileInput');
const fileSelected = document.getElementById('fileSelected');
const fileName = document.getElementById('fileName');
const fileRemove = document.getElementById('fileRemove');

// Click to upload
if (fileUploadArea) {
    fileUploadArea.addEventListener('click', (e) => {
        if (!e.target.classList.contains('file-remove')) {
            fileInput.click();
        }
    });
}

// File selection
if (fileInput) {
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            fileName.textContent = file.name;
            fileUploadArea.querySelector('.file-upload-content').style.display = 'none';
            fileSelected.style.display = 'flex';
            newsText.value = '';
            newsText.disabled = true;
        }
    });
}

// Drag and drop
if (fileUploadArea) {
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.classList.add('drag-over');
    });

    fileUploadArea.addEventListener('dragleave', () => {
        fileUploadArea.classList.remove('drag-over');
    });

    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.classList.remove('drag-over');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileName.textContent = files[0].name;
            fileUploadArea.querySelector('.file-upload-content').style.display = 'none';
            fileSelected.style.display = 'flex';
            newsText.value = '';
            newsText.disabled = true;
        }
    });
}

// Remove file
if (fileRemove) {
    fileRemove.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.value = '';
        fileUploadArea.querySelector('.file-upload-content').style.display = 'flex';
        fileSelected.style.display = 'none';
        newsText.disabled = false;
    });
}
