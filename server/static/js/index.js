const socket = io(); //socketio connection to server//

socket.on('connect', function() {
    socket.emit('ass', {
        data: 'User connected'
    });
});

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
        window.location.href = `/waiting?sid=${socket.id}`
    })
    .catch(error => console.error('Error:', error));
});