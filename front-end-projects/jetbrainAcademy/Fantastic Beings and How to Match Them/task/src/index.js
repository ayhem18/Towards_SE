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


// a global variable to save the number of cleared cells in each column, row
const CLEARED_BY_ROW = new Map();
const CLEARED_BY_COLUMN = new Map();


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
            // add an attribute to the cell node that determines its coordinates
            cell.setAttribute("data-coords", `x${j}_y${i}`)
            cell.setAttribute("data-x", `${j}`);
            cell.setAttribute("data-y", `${i}`);

            // add it as a child to the row html element
            row.appendChild(cell);
        }
        // having all the cells in the row added, add the row to the board html element
        board.appendChild(row);
    }
    // after initializing the map, set the values in the CLEARED_BY_ROW and CLEARED_BY_COLUMN accordingly
    // writing this piece of code in the initializeMap function ensures that those variables will be set correctly
    // when redrawing the map
    CLEARED_BY_ROW.clear();
    CLEARED_BY_COLUMN.clear();

    for (let i = 0; i < n_rows; i++) {
        CLEARED_BY_ROW.set(i, 0)
    }

    for (let i = 0; i < n_cols; i++) {
        CLEARED_BY_COLUMN.set(i, 0)
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


// a global variable saving the currently clicked cell
let CLICKED_CELL = null;

// functions to handle the game play
function getCoordinates(cell) {
    let y = parseInt(cell.dataset["y"]);
    let x = parseInt(cell.dataset["x"]);
    return Array.of(y, x);
    // let coords_1 = cell.dataset['coords'];
    //
    // if (coords_1 === undefined) {
    //     throw `The HTML elements are expected to have data-coords  attributes.`;
    // }
    //
    // let c1 = coords_1.split("_");
    //
    // let x1 = parseInt(c1[0][1]);
    // let y1 = parseInt(c1[1][1]);
    //
    // return Array.of(y1, x1);
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
    let maxX = board.children[0].children.length;

    // first step is to extract the cell
    let initialCell = getCell(y, x);
    let beingName = initialCell.getAttribute("data-being");

    if (beingName === null) {
        throw "a selected cell with a null beingName";
    }

    // first consider the vertical direction

    // upwards
    let up_y = y;

    while ((up_y - 1 >= 0) &&
    (getCell(up_y - 1, x).getAttribute("data-being")) === beingName) {
        up_y -= 1;
    }

    // downwards
    let down_y = y;

    while ((down_y + 1 < maxY) &&
    (getCell(down_y + 1, x).getAttribute("data-being")) === beingName) {
        down_y += 1;
    }

    // // consider the horizontal direction: to the right
    // let right_x = x;
    //
    // while ((right_x + 1 < maxX) &&
    // (getCell(y, right_x + 1).getAttribute("data-being")) === beingName) {
    //     right_x += 1;
    // }
    //
    // // to the left
    // let left_x = x;
    //
    // while((left_x -1 >= 0) &&
    // (getCell(y, left_x - 1).getAttribute("data-being")) === beingName) {
    //     left_x -= 1;
    // }
    
    let clearedCellsCoordinates= [];

    // create an array to save the coordinates of the cell to be cleared
    // if (right_x - left_x + 1 >= 3) {
    //     for (let i = left_x; i <= right_x; i++) {
    //         clearedCellsCoordinates.push([y, i]);
    //     }
    // }

    if (down_y - up_y + 1 >= 3) {
        for(let i = up_y; i <= down_y; i++) {
            clearedCellsCoordinates.push([i, x]);
        }
    }

    return clearedCellsCoordinates;
}

function update_after_clearing_rows(rowIndex) {
    // the idea here is to update the coordinates of each row with an index larger than the passed one
    const board = document.getElementById("map");
    for (let i = rowIndex + 1; i < board.children.length; i++) {
        for (let j = 0; j < board.children[i].children.length; j++) {
            let cell = board.children[i].children[j];
            // update the data-coords field for the cell element
            cell.setAttribute("data-coords", `x${j}_y${i-1}`)
            // update the same attribute for the image if it exists (the cell might be cleared already)
            if (cell.innerHTML !== "") {
                cell.children[0].setAttribute("data-coords", `y${j}_y${i-1}`);
            }
        }
    }
    // remove the <tr> element from the board
    board.children[rowIndex].remove();

    // update the CLEARED_BY_ROW variable as follows:
    // for each row larger than rowIndex, move the value CLEARED_BY_ROW[i] to the key i - 1
    for (let i = rowIndex + 1; i < board.children.length; i++) {
        CLEARED_BY_ROW.set(i - 1, CLEARED_BY_ROW.get(i));
    }
    // remove the last row
    CLEARED_BY_ROW.delete(board.children.length - 1);

    // decrement the number of cleared cells in each column
    for (let i = 0; i <= board.children[0].length; i++) {
        CLEARED_BY_COLUMN.set(i, CLEARED_BY_COLUMN.get(i) - 1);
    }
}

function update_after_clearing_columns(columnIndex) {
    // the idea here is update all the columns
    const board = document.getElementById("map");
    for (let i = 0; i < board.children.length; i++) {
        for (let j = columnIndex + 1; j < board.children[i].children.length; j++) {
            let cell = board.children[i].children[j];
            // update the data-coords field for the cell element
            cell.setAttribute("data-coords", `x${j - 1}_y${i}`)
            // update the same attribute for the image if it exists (the cell might be cleared already)
            if (cell.innerHTML !== "") {
                cell.children[0].setAttribute("data-coords", `y${j - 1}_y${i}`);
            }
        }
        // remove the <td> cell completely from the dom
        board.children[i].children[columnIndex].remove();
    }

    // update the CLEARED_BY_COLUMN variable as follows
    // for each row column larger than columnIndex, move the value CLEARED_BY_COLUMN[i] to the key i - 1
    for (let i = columnIndex + 1; i < board.children[0].length; i++) {
        CLEARED_BY_COLUMN.set(i - 1, CLEARED_BY_COLUMN.get(i));
    }
    CLEARED_BY_COLUMN.delete(board.children[0].length - 1);

    // decrement the number of cleared cells in each row
    for (let i = 0; i <= board.children.length; i++) {
        CLEARED_BY_ROW.set(i, CLEARED_BY_ROW.get(i) - 1);
    }
}

function clearCells(cellCoordinates) {

    // const board = document.getElementById("map");
    // let maxRows = board.children.length;
    // let maxCols = board.children[0].children.length;

    for (let i = 0; i < cellCoordinates.length; i++) {
        let y = cellCoordinates[i][0];
        let x = cellCoordinates[i][1];
        let cell = getCell(y, x);
        // make sure to remove the image
        cell.innerHTML = "";
        // make sure to set the attribute to None, so it won't be used
        cell.setAttribute("data-being", '');

        // make sure to increase the number of cleared cells by row and column
        // the column is determined by "x"
        // CLEARED_BY_COLUMN.set(x, CLEARED_BY_COLUMN.get(x) + 1);
        // CLEARED_BY_ROW.set(y, CLEARED_BY_ROW.get(y) + 1);
    }

    // // make sure to start with later rows
    //
    // for (let i = maxRows - 1; i >= 0; i--) {
    //     if (CLEARED_BY_ROW.get(i) === maxRows) { // this means the i-th row has been fully cleared
    //         // get the current coordinates
    //         update_after_clearing_rows(i);
    //     }
    // }
    //
    // // make sure to start with later columns
    // for (let i = maxCols - 1; i >=0 ; i--) {
    //     if (CLEARED_BY_COLUMN.get(i) === maxCols) { // this means the i-th row has been fully cleared
    //         // get the current coordinates
    //         update_after_clearing_columns(i);
    //     }
    // }
}

function swap(cell1, cell2) {
    // swap the inner html
    let temp = cell1.innerHTML;
    cell1.innerHTML = cell2.innerHTML;
    cell2.innerHTML = temp;

    // swap the being attributes on the cell element
    temp = cell1.getAttribute("data-being");
    cell1.setAttribute("data-being", cell2.getAttribute("data-being"));
    cell2.setAttribute("data-being", temp);

    // make sure to update the data-coords attribute of the image child node as well
    cell1.children[0].setAttribute("data-coords", cell1.getAttribute("data-coords"));
    cell2.children[0].setAttribute("data-coords", cell2.getAttribute("data-coords"));
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
    let targetCell = event.target;

    // check if the target cell is an image element
    if (targetCell.tagName.toLowerCase() === "img") {
        targetCell = targetCell.parentNode;
    }

    if (targetCell.innerHTML === "") {
        alert("An empty cell cannot be selected");
        return;
    }

    // step2 proceed depending on the value of CLICKED_CELL
    if (CLICKED_CELL === null) {
        //console.log("first cell clicked");
        CLICKED_CELL = targetCell;
        selectCell(targetCell);
        return;
    }

    // at this point the CLICKED_CELL was set before the event
    if (CLICKED_CELL === targetCell) {
        // will be interpreted as deselecting the cell
        //console.log("cell deselected")
        deselectCell(targetCell);
        CLICKED_CELL = null;
        return;
    }

    // at this point the CLICKED_CELL is set and the target cell is different from CLICKED_CELL
    // step1: make sure the cells are adjacent
    // the coordinate attributes are saved at the image level and not the cell level (unfortunately)
    if (! areCellsAdjacent(CLICKED_CELL, targetCell)) {
        return;
    }

    swap(CLICKED_CELL, targetCell);
    deselectCell(CLICKED_CELL);

    // find whether the target cell is part of some sequence
    let targetCoords = getCoordinates(targetCell);
    let ty = targetCoords[0];
    let tx = targetCoords[1];
    let sequences1 = findSequences(ty, tx);


    // find whether the clicked cell is part of some sequence
    targetCoords = getCoordinates(CLICKED_CELL);
    ty = targetCoords[0];
    tx = targetCoords[1];
    let sequences2 = findSequences(ty, tx)

    // push all elements of the 2nd sequence to the first one
    sequences1.push(...sequences2);

    if (sequences1.length === 0) {
        // swap the clicked and target cell back
        swap(CLICKED_CELL, targetCell);

    } else {
        // clear the sequences
        clearCells(sequences1);
    }

    CLICKED_CELL = null;
}

// add the event listener
// the event handling mechanism should probably be moved to th board element
// using event bubbling (at the time of writing this code, I do not remember the mechanism in question)
function setClickEventListeners() {
    let board = document.getElementById("map");
    for (let i = 0; i < board.children.length; i++) {
        for (let j = 0; j < board.children[i].children.length; j++) {
            // board.children[i].children[j].addEventListener("click", clickCellEventHandler);
            let cell = board.children[i].children[j];
            cell.addEventListener("click", clickCellEventHandler);
        }
    }
}


// call the function to create the board
window.renderMap(5, 5)

// window.renderMap(3, 3)

// window.redrawMap([
//     ['kelpie', 'puffskein', 'puffskein'],
//     ['swooping', 'zouwu', 'puffskein'],
//     ['kelpie', 'puffskein', 'zouwu']
// ]);
// don't forget to set the event handlers
setClickEventListeners();
