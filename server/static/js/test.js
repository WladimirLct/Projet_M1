//JS pour la loading bar
document.getElementById('analyzeButton').addEventListener('click', startAnalyzing);

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