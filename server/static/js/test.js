//JS pour la loading bar
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