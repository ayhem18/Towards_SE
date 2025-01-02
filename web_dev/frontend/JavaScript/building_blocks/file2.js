// add a listener to the container 

// const container_element = document.querySelector(". container");

// function chance_text_color(event) {
//     // extract the target
//     let target_element = event.target
//     let color = target_element.getAttribute("data-color")
//     target_element.style.color = color;
// }


// container_element.addEventListener("click", chance_text_color)


// this is a script to run few lines of code
function checkTheDate(value){
    switch ((1 <= value) && (value <= 5)) {
        case true:
            console.log("Yes, you should go to work");
            break;
        default:
            console.log("No, this is your well-deserved weekend!");
    }
}

const planets = ["Earth", "Jupiter", "Neptune"];

function showPlanets(planets) {
    planets.forEach(function(v) {console.log(v);});
}

showPlanets(planets);
