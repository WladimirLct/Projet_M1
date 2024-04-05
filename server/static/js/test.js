//JS TEST/EX POUR LES FETCHS

function click() {
    const test = document.getElementById('test');
    test.addEventListener('click', () => {
        return fetchTestElement();
    });
}

function fetchTestElement() {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body : JSON.stringify({ test: true })
    };
    fetch('/test', options)
        .then(response => {
            return response.json();
        }).then(data => {
            console.log(data);
            return data;
        });
}


click();