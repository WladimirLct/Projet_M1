const socket = io(); //socketio connection to server//

const loadingBarContainer = document.getElementById('loadingBarContainer');
const loadingBar = document.getElementById('loadingBar');

let form = document.getElementById('dropzone-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    // Set the cursor to loading
    document.body.style.cursor = 'wait';

    let formData = new FormData();
    let fileField = document.querySelector('input[type="file"]');

    formData.append('file', fileField.files[0]);

    loadingBarContainer.classList.remove('hidden'); // Show loading bar container
    loadingBar.style.width = '0%'; // Reset width

    let progress = 0;
    const interval = setInterval(() => {
        progress += 1; // Increment progress more slowly
        loadingBar.style.width = `${progress}%`;

        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 50); // Adjust speed for a more gradual progress

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        loadingBar.style.width = '100%';
        // Redirect to /waiting after 3 seconds
        setTimeout(() => {
            window.location.href = '/waiting';
        }, 3000);

    })
    .catch(error => console.error('Error:', error));
});