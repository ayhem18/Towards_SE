/*
* This script is used to automate the board creation
*/

// an array to save the creatures names
const CREATURE_NAMES = ["kelpie", "puffskein", "salamander", "swooping", "zouwu"]

// a mapping between the creature name and its image location
const creatureToImg = new Map();
creatureToImg.set(CREATURE_NAMES[0], `./images/${CREATURE_NAMES[0]}.png`)
creatureToImg.set(CREATURE_NAMES[1], `./images/${CREATURE_NAMES[1]}.png`)
creatureToImg.set(CREATURE_NAMES[2], `./images/${CREATURE_NAMES[2]}.png`)
creatureToImg.set(CREATURE_NAMES[3], `./images/${CREATURE_NAMES[3]}.png`)
creatureToImg.set(CREATURE_NAMES[4], `./images/${CREATURE_NAMES[4]}.png`)

function getRandomCreature() {
    let creatureIndex = Math.floor(Math.random() * creatureToImg.size);
    return CREATURE_NAMES[creatureIndex];
}

// a function to populate the board with creatures randomly
function getRandomCreaturesMap(nRows, nCols) {
    // inspired by: https://stackoverflow.com/questions/18163234/declare-an-empty-two-dimensional-array-in-javascript
    const matrix = new Array(nRows).fill(0).map(() => new Array(nCols).fill(0));

    for (let i = 0; i < nRows; i++) {
        for (let j = 0; j < nCols; j++) {
            // get the random being
            matrix[i][j] = getRandomCreature();
        }
    }
    return matrix;
}

// a function to set the "board" element as a table.
function initializeMap(n_rows, n_cols) {
    let board = document.getElementById("map");
    for (let i = 0; i < n_rows; i++) {
        // create a row html element
        let row = document.createElement("tr");
        for (let j = 0; j < n_cols; j++) {
            let cell = document.createElement("td");
            // make sure to set its class to "cell"
            cell.classList.add("cell");
            // add it as a child to the row html element
            row.appendChild(cell);
        }
        // having all the cells in the row added, add the row to the board html element
        board.appendChild(row);
    }
}


function renderMap(nRows, nCols) {
    const randomCreaturesMap = getRandomCreaturesMap(nRows, nCols);
    // let nRows = creaturesMap.length;
    // let nCols = creaturesMap[0].length;

    // first initialize the map: DOM manipulation
    initializeMap(nRows, nCols);

    let board = document.getElementById("map");

    for (let i = 0; i < nRows; i++) {
        let row = board.children[i];

        // create a row html element
        for (let j = 0; j < nCols; j++) {
            let beingName = randomCreaturesMap[i][j];
            // get the cell
            let cell = row.children[j];

            // 1. set the "data-being" attribute
            // 2. add the img HTML element to the cell's children

            // set additional attributes to the cell node
            cell.setAttribute("data-being", beingName);


            // create an image element
            let creatureImage = document.createElement("img");
            creatureImage.setAttribute("src",creatureToImg.get(beingName));
            creatureImage.setAttribute("data-coords", `x${j}_y${i}`);
            creatureImage.style.width = "80%";
            creatureImage.style.margin = "0 10% 0 10%";
            cell.appendChild(creatureImage);
        }
    }
}


function redrawMap(creaturesMap) {
    // make sure the creaturesMap object is a multidimensional array
    if (! (Array.isArray(creaturesMap) && Array.isArray(creaturesMap[0]))) {
        return false;
    }

    let nRows = creaturesMap.length;
    let nCols = creaturesMap[0].length;

    let board = document.getElementById("map");

    // make sure the size of the new array is the same the passed array
    if (board.children.length !== nRows || board.children[0].children.length !== nCols) {
        return false;
    }

    for (let i = 0; i < nRows; i++) {
        let row = board.children[i];

        // create a row html element
        for (let j = 0; j < nCols; j++) {
            let beingName = creaturesMap[i][j];
            // get the cell
            let cell = row.children[j];

            if (cell.children.length !== 0) {
                // if the cell is already filled with the same being, no need to modify the dom
                if (cell.getAttribute("data-being") !== beingName) {
                    cell.setAttribute("data-being", beingName);
                    cell.children[0].setAttribute("src", creatureToImg.get(beingName));
                }
            }
        }
    }
    // at this point everything is good
    return true;
}


// a function to clear the map
function clear_map() {
    let board = document.getElementById("map");
    // set the html
    board.innerHTML = "";
}

window.renderMap = renderMap;
window.redrawMap = redrawMap;
window.clearMap = clear_map;

// let user_clear_map = confirm("clear the board ?")
//
// if (user_clear_map){
//     window.clearMap();
// }

// call the function to create the board
// const creaturesMap = getRandomCreaturesMap(5, 5);
window.renderMap(5, 5)

