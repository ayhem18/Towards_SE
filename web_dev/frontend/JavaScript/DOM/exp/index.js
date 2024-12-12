// create a list
let section = document.createElement("div")
section.style.backgroundColor = "red"
section.style.width = "10vw"
section.style.height = "10vh"

document.body.appendChild(section)


// create another element
let ul = document.createElement("ul")

// add an element
let item1 = document.createElement("li")
item1.textContent = "item1"
ul.appendChild(item1)
section.appendChild(ul)


let rm = confirm("Remove the red block ???")

if (rm) {
    section.removeChild(ul)
}

