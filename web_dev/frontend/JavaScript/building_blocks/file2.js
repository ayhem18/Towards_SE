// add a listener to the container 

const container_element = document.querySelector(". container");

function chance_text_color(event) {
    // extract the target
    let target_element = event.target
    let color = target_element.getAttribute("data-color")
    target_element.style.color = color;
}


container_element.addEventListener("click", chance_text_color)
