const GraphLesionData = {
    labels: ['M', 'E', 'S', 'C'],
    datasets: [{
        label: 'Nombre de glomérules pour la lésion',
        data: [65, 59, 80, 81],
        backgroundColor: [
            'rgba(59, 130, 246, 0.9)',
            'rgba(59, 130, 246, 0.9)',
            'rgba(59, 130, 246, 0.9)',
            'rgba(59, 130, 246, 0.9)',
        ],
        borderColor: [
            'rgb(59, 130, 246)',
            'rgb(59, 130, 246)',
            'rgb(59, 130, 246)',
            'rgb(59, 130, 246)',
        ],
        borderWidth: 2
    }]
};

const GraphLesionAccuracyData = {
    labels: ['M', 'E', 'S', 'C'],
    datasets: [{
        label: 'Nombre de glomérules pour la lésion',
        data: [65, 59, 80, 81],
        backgroundColor: [
            'rgba(59, 130, 246, 0.9)',
            'rgba(59, 150, 246, 0.9)',
            'rgba(59, 170, 246, 0.9)',
            'rgba(59, 190, 246, 0.9)',
        ],
        borderColor: [
            'rgb(59, 130, 246)',
            'rgb(59, 150, 246)',
            'rgb(59, 170, 246)',
            'rgb(59, 190, 246)',
        ],
        borderWidth: 2
    }]
};

const config = {
    type: 'bar',
    data: GraphLesionData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        responsive: false,
        maintainAspectRatio: true,
        
        plugins: {
            title: {
                display: true,
                text: 'Nombre de glomérules par lésion',
                color: 'rgb(59, 130, 246)',
                font: {
                    weight: 'bold',
                    size: 20
                }
            },
            legend: {
                display: false
            },
           
        }
    }
};


const config2 = {
    type: 'polarArea',
    data: GraphLesionAccuracyData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        responsive: false,
        maintainAspectRatio: true,
        legend: {
            display: true, // Afficher la légende
            labels: {
                // Étiquettes personnalisées pour chaque dataset
                generateLabels: function (chart) {
                    const labels = chart.data.datasets.map(function (dataset, index) {
                        return {
                            text: dataset.label, // Texte de l'étiquette
                            fillStyle: dataset.borderColor, // Couleur de remplissage de l'étiquette
                            strokeStyle: dataset.borderColor, // Couleur de bordure de l'étiquette
                            lineWidth: 1, // Épaisseur de la bordure de l'étiquette
                            hidden: false, // Masquer ou afficher l'étiquette
                            index: index // Indice du dataset
                        };
                    });
                    return labels;
                }
            }
        }
    }
};

const canvasElement = document.getElementById('GraphLesion');
const GraphLesion = new Chart(canvasElement, config);

const canvasElement2 = document.getElementById('GraphAccuracy');
const GraphAccuracy = new Chart(canvasElement2, config2);