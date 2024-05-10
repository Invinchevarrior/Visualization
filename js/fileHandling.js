
export function handleUpload(event) {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.onchange = e => {
        const file = e.target.files[0];
        uploadFile(file);
    }
    fileInput.click();
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://10.112.127.227:8000/home/lab212/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

export function fetchAndDisplayFiles() {
    fetch('http://10.112.127.227:8000/home/lab212/upload', { method: 'GET' })
        .then(response => response.json())
        .then(files => {
            const fileListElement = document.getElementById('file-list');
            fileListElement.innerHTML = ''; // Clear current list

            fileListElement.style.display = 'flex';
            fileListElement.style.flexDirection = 'column';
            fileListElement.style.alignItems = 'flex-start'; // Align items to the start of the flex container

            files.forEach(file => {
                const fileElement = document.createElement('div');
                fileElement.textContent = file.name; // Display the name of the file or folder
                fileElement.style.cursor = 'pointer';
                fileElement.style.marginBottom = '5px'; // Add margin between filenames

                fileElement.onclick = () => {
                    if (file.isFolder) {
                        // If it's a folder, fetch its contents and display
                        fetchAndDisplaySubFolder(file.name);
                    } else {
                        openFile(file.name); // If it's a file, open it
                    }
                };

                fileListElement.appendChild(fileElement);
            });
        })
        .catch(error => console.error('Error fetching files:', error));
}

function fetchAndDisplaySubFolder(folderName) {
    const folderUrl = encodeURI(`http://10.112.127.227:8000/home/lab212/upload/${folderName}`);
    
    fetch(folderUrl, { method: 'GET' })
        .then(response => response.json())
        .then(contents => {
            // Update the file list with the contents of the folder
            const fileListElement = document.getElementById('file-list');
            fileListElement.innerHTML = ''; // Clear current list

            contents.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.textContent = item.name;
                itemElement.style.cursor = 'pointer';
                itemElement.style.marginBottom = '5px';

                itemElement.onclick = () => {
                    if (item.isFolder) {
                        fetchAndDisplaySubFolder(`${folderName}/${item.name}`);
                    } else {
                        openFile(`${folderName}/${item.name}`);
                    }
                };

                fileListElement.appendChild(itemElement);
            });
        })
        .catch(error => console.error(`Error fetching folder contents: ${folderName}`, error));
}

function openFile(filePath) {
    const fileUrl = encodeURI(`http://10.112.127.227:8000/home/lab212/upload/${filePath}`);
    window.open(fileUrl, '_blank');
}



