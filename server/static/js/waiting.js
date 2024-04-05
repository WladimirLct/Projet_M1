const carousels = document.querySelectorAll(".carousel");

let carouselIntervals = [];
let duration = [2000, 1250];


// Move the carousel 25% to the top using tailwind classes and animations
function moveCarouselUp(carousel, duration) {
    carousel.classList.remove("translate-y-0");
    carousel.classList.add("translate-y-[-25%]");
    carousel.classList.add("transition", `duration-[${duration}ms]`);
}


function resetCarousel(carousel, duration) {
    let imgs = carousel.querySelectorAll("img");

    // Put the first image at the end and remove it from the beginning
    let firstImg = imgs[0];
    carousel.appendChild(firstImg);

    // Reset the carousel position instantly
    carousel.classList.remove("transition", `duration-[${duration}ms]`);
    carousel.classList.remove("translate-y-[-25%]");
    carousel.classList.add("translate-y-0");
}


// Do a loop of the carousel
function loopCarousel(carousel, duration) {
    moveCarouselUp(carousel, duration);
    setTimeout(() => {
        resetCarousel(carousel, duration);
    }, duration);
}


let step_counter = -1;
let steps = ["tiles", "masks", "crops", "score", "redirect", false];

socket.on('message', (data) => {
    if (data.step != -1) {
        if (step_counter > data.step) {
            return;
        }
        step_counter = data.step;
    }

    var ul = document.getElementById("log");
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(data.text));


    // Appliquer une translation initiale sur l'axe X
    li.classList.add("transform", "-translate-y-full", "text-[#0b1d3e]", "text-4xl", "font-bold", "transition", "duration-500", "ease-in-out");
    ul.insertBefore(li, ul.firstChild);


    // Animer la translation X pour la ramener à sa position initiale
    setTimeout(() => {
        li.classList.remove("-translate-y-full");
        li.classList.add("translate-y-0");
    }, 10);
    

    // Décaler les autres éléments pour laisser la place au nouveau
    var otherLis = ul.getElementsByTagName("li");
    for (var i = 1; i < otherLis.length; i++) {
        otherLis[i].classList.remove("text-4xl", "font-bold");
        otherLis[i].classList.add("text-xl");

        var opacity = Math.max(1 - i * 0.2, 0.1);
        otherLis[i].style.opacity = opacity.toString();
        otherLis[i].style.transform = "translateY(" + 20 + "px)";
    }

    if (steps[step_counter] == "tiles") {
        // Show all images then start the carousel loop (using tailwind classes)
        carousels.forEach(carousel => {
            carousel.classList.remove("hidden");
        });

        // Start the carousel loop
        carousels.forEach((carousel, index) => {
            loopCarousel(carousel, duration[index]);

            let interval = setInterval(() => {
                loopCarousel(carousel, duration[index]);
            }, (duration[index] + 9));

            carouselIntervals.push(interval);
        });
    }

    if (steps[step_counter] != "score" && steps[step_counter] != "redirect"  && steps[step_counter]) {
        fetch("/" + steps[step_counter])
            .then(response => response.json())
            .then(data => {
                for (let i = 0; i < data.result.length; i++) {
                    let img = document.getElementById("img" + i);
                    img.src = data.result[i];
                }
            });
    } else if (steps[step_counter] == "score") {
        fetch("/score")
            .then(response => response.json())
            .then(data => {
                console.log(data);
            });
    } else if (steps[step_counter] == "redirect") {
        window.location.replace("/results");
    }
});