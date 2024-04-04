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