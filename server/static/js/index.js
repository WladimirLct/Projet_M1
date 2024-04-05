const socket = io(); //socketio connection to server//

let form = document.getElementById('dropzone-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData();
    let fileField = document.querySelector('input[type="file"]');

    formData.append('file', fileField.files[0]);

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        window.location.replace('/waiting');
    })
    .catch(error => console.error('Error:', error));
});

//JS for the loading bar
document.getElementById('analyze-btn').addEventListener('click', startAnalyzing);

function startAnalyzing() {
    const loadingBarContainer = document.getElementById('loadingBarContainer');
    const loadingBar = document.getElementById('loadingBar');

    loadingBarContainer.classList.remove('hidden'); // Show loading bar container
    loadingBar.style.width = '0%'; // Reset width

    let progress = 0;
    const interval = setInterval(() => {
        progress += 1; // Increment progress more slowly
        loadingBar.style.width = `${progress}%`;

        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                loadingBarContainer.classList.add('hidden');
                loadingBar.style.width = '0%';
            }, 2000); // Keep the loading bar visible a bit longer after reaching 100%
        }
    }, 20); // Adjust speed for a more gradual progress
}