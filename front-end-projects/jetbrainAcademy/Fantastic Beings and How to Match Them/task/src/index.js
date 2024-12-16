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


// global variable saving the currently clicked cell
let CLICKED_CELL = null;

// functions to handle the game play
function getCoordinates(cell) {
    let coords_1 = cell.dataset['coords'];

    if (coords_1 === undefined) {
        throw `The HTML elements are expected to have data-coords  attributes.`;
    }

    let c1 = coords_1.split("_");

    let x1 = parseInt(c1[0][1]);
    let y1 = parseInt(c1[1][1]);

    return Array.of(y1, x1);
}


// check if two cells are adjacent
function areCellsAdjacent(cell1, cell2) {
    let c1 = getCoordinates(cell1);
    let c2 = getCoordinates(cell2);

    let y1 = c1[0];
    let x1 = c1[1];

    let y2 = c2[0];
    let x2 = c2[1];

    // rule the case where both cells are the same
    if (x1 === x2 && y1 === y2) {
        return false;
    }

    return ((Math.abs(x1 - x2) <= 1) && (y1 === y2)) || ((x1 === x2) && (Math.abs(y1 - y2) <= 1));
}

// a function that returns the cell given the coordinates
function getCell(y, x) {
    // extract the board element
    let board = document.getElementById("map");
    return board.children[y].children[x];
}

function findSequences(y, x) {
    let board = document.getElementById("map");
    let maxY = board.children.length;
    let maxX = board.children[0].length;

    // first step is to extract the cell
    let initialCell = getCell(y, x);
    let beingName = initialCell.getAttribute("data-being");

    // first consider the vertical direction

    // upwards
    let up_y = y;

    while (up_y >= 0) {
        let currentBeingName = getCell(up_y, x).getAttribute("data-being");
        if (beingName !== currentBeingName) {
            break;
        }
        up_y -= 1;
    }

    // downwards
    let down_y = y;

    while (down_y < maxY) {
        let currentBeingName = getCell(down_y, x).getAttribute("data-being");
        if (beingName !== currentBeingName) {
            break;
        }
        down_y += 1;
    }

    // consider the horizontal direction
    // to the right
    let right_x = x;

    while (right_x < maxX) {
        let currentBeingName = getCell(y, right_x).getAttribute("data-being");
        if (beingName !== currentBeingName) {
            break;
        }
        right_x += 1;
    }

    // to the left
    let left_x = x;

    while (left_x >= 0) {
        let currentBeingName = getCell(y, left_x).getAttribute("data-being");
        if (beingName !== currentBeingName) {
            break;
        }
        left_x -= 1;
    }

    let cleared_cells = [];

    // create an array to save the coordinates of the cell to be cleared
    if (right_x - left_x + 1 >= 3) {
        for (let i = left_x; i <= right_x; i++) {
            cleared_cells.push([y, i]);
        }
    }

    if (down_y - up_y + 1 >= 3) {
        for(let i = up_y; i <= down_y; i++) {
            cleared_cells.push([i, x]);
        }
    }

    return cleared_cells;
}

function clearCells(cellCoordinates) {
    for (let i = 0; i < cellCoordinates.length; i++) {
        let y = cellCoordinates[i][0];
        let x = cellCoordinates[i][1];
        let cell = getCell(y, x);
        cell.innerHTML = "";
    }
}

function swap(cell1, cell2) {
    // the idea is simple, just swap the innerHTML values
    let c1 = getCoordinates(cell1.children[0]);
    let c2 = getCoordinates(cell2.children[0]);

    let y1 = c1[0];
    let x1 = c1[1];

    let y2 = c2[0];
    let x2 = c2[1];

    let c1_str = `x${x1}_y${y1}`;
    let c2_str = `x${x2}_y${y2}`;

    // make sure to update the `data-coords` attribute in the swapped images
    cell1.children[0].setAttribute("data-coords", c1_str);
    cell2.children[0].setAttribute("data-coords", c2_str);

    // swap the inner html
    let temp = cell1.innerHTML;
    cell1.innerHTML = cell2.innerHTML;
    cell2.innerHTML = temp;

}

function selectCell(cell) {
    // highlight the target cell using css
    cell.style.backgroundImage = "url(./images/cell-selected-bg.png)";
    cell.style.backgroundSize = "cover";
}

function deselectCell(cell) {
    // highlight the target cell using css
    cell.style.backgroundImage = null;
    cell.style.backgroundSize = null
}


function clickCellEventHandler(event) {

    // step1: extract the event target
    let targetCell = event.target.parentNode;
    console.log(`The cell ${targetCell.dataset} is clicked!`);

    // step2 proceed depending on the value of CLICKED_CELL
    if (CLICKED_CELL === null) {
        console.log("first cell clicked");
        CLICKED_CELL = targetCell;
        selectCell(targetCell);
        return;
    }

    // at this point the CLICKED_CELL was set before the event
    if (CLICKED_CELL === targetCell) {
        // will be interpreted as deselecting the cell
        console.log("cell deselected")
        deselectCell(targetCell);
        return;
    }

    // at this point the CLICKED_CELL is set and the target cell is different from CLICKED_CELL
    // step1: make sure the cells are adjacent
    // the coordinate attributes are saved at the image level and not the cell level (unfortuately)
    if (! areCellsAdjacent(CLICKED_CELL.children[0], targetCell.children[0])) {
        return;
    }

    swap(CLICKED_CELL, targetCell);
    deselectCell(CLICKED_CELL);
    CLICKED_CELL = null;


}


// add the event listener
// the event handling mechanism should probably be moved to th board element
// using event bubbling (at the time of writing this code, I do not remember the mechanism in question)
function setClickEventListeners() {
    let board = document.getElementById("map");
    for (let i = 0; i < board.children.length; i++) {
        for (let j = 0; j < board.children[i].children.length; j++) {
            board.children[i].children[j].addEventListener("click", clickCellEventHandler);
        }
    }
}


// call the function to create the board
window.renderMap(5, 5)
// don't forget to set the event handlers
setClickEventListeners();
