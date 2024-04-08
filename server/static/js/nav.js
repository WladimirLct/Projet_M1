function clickOnPopUp(){
    const history = document.getElementById("history");
    history.addEventListener("click", () => {
        const popup = document.getElementById("popup")
        popup.classList.toggle('hidden');
        
    })
}

clickOnPopUp()