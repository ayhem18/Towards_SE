// a function to set the "board" element as a table.

// global variable to keep track of the game state
let SCORE = 0;
let MAX_NUM_MOVES = null;
let BEINGS_TARGET_COUNTS = null;


function setCellAttributes(cell, y, x) {
    cell.setAttribute("data-coords", `x${x}_y${y}`)
    cell.setAttribute("data-y", `${y}`);
    cell.setAttribute("data-x", `${x}`);
}

function setCellBeingInfo(cell, beingName,) {
    if (cell.getAttribute("data-coords") === null) {
        throw "The cell must have a 'data-coords' attribute";
    }
    // set additional attributes to the cell node
    cell.setAttribute("data-being", beingName);
    // create an image element
    let creatureImage = document.createElement("img");
    creatureImage.setAttribute("src",creatureToImg.get(beingName));
    // set the image data-coords attribute to the same value as that of "data-coords"
    creatureImage.setAttribute("data-coords", cell.getAttribute("data-coords"));

    // make sure the image has a certain class to apply specific styling
    creatureImage.classList.add("being_cell_img")

    // add "img" element to the cell
    cell.appendChild(creatureImage);
}

function initializeMap(n_rows, n_cols) {
    // console.log("map initialized !!!!")

    let board = document.getElementById("map");
    for (let i = 0; i < n_rows; i++) {
        // create a row html element
        let row = document.createElement("tr");
        for (let j = 0; j < n_cols; j++) {
            let cell = document.createElement("td");
            // make sure to set its class to "cell"
            cell.classList.add("cell");
            // add an attribute to the cell node that determines its coordinates
            setCellAttributes(cell, i, j);
            // add it as a child to the row html element
            row.appendChild(cell);
        }
        // having all the cells in the row added, add the row to the board html element
        board.appendChild(row);
    }
}

function setClickEventListeners(eventHandler) {
    let board = document.getElementById("map");
    for (let i = 0; i < board.children.length; i++) {
        for (let j = 0; j < board.children[i].children.length; j++) {
            board.children[i].children[j].addEventListener("click", eventHandler);
        }
    }
}

function setBeingsTargetBar(beingTargetCounts) {

    // step1: create a div
    let mainDiv = document.createElement("div");
    mainDiv.setAttribute("id", "being_count_bar")


    let imageCount = 0;

    for (let [key, value] of beingTargetCounts.entries()) {
        imageCount += 1;

        let beingImage = document.createElement("image");
        //
        beingImage.setAttribute("src", creatureToImg.get(key));
        beingImage.setAttribute("class", "being_status_bar_img");
        beingImage.setAttribute("id", `img${imageCount}`);

        let beingCountDiv = document.createElement("div");
        beingCountDiv.setAttribute("class", "being_count_div");

        let beingCountSpan = document.createElement("span");
        beingCountSpan.setAttribute("class", "being_count");
        beingCountSpan.appendChild(document.createTextNode(`${0}`));
        beingCountDiv.appendChild(beingCountSpan);

        // add to MainDiv
        mainDiv.appendChild(beingImage);
        mainDiv.appendChild(beingCountSpan);

    }

    const statusBarContent = document.createElement("status-bar-content");
    statusBarContent.appendChild(mainDiv);
}

function setNumMovesBar(maxNumMoves) {
    /*create the bar with the number of moves left*/
    let movesCountDiv = document.createElement("div");
    movesCountDiv.setAttribute("id", "moves_count_bar");

    let movesCountTextSpan = document.createElement("span");
    movesCountTextSpan.setAttribute("id", "moves_count_text");
    movesCountTextSpan.appendChild(document.createTextNode("Moves"));

    let movesCountSpan = document.createElement("span");
    movesCountTextSpan.setAttribute("id", "moves_count");
    movesCountTextSpan.appendChild(document.createTextNode(`${maxNumMoves}`));

    // add both spans to the movesCountDiv
    movesCountDiv.appendChild(movesCountTextSpan);
    movesCountDiv.appendChild(movesCountSpan);

    const statusBarContent = document.createElement("status-bar-content");
    statusBarContent.appendChild(movesCountDiv);
}

function setGameStateCanvas(beingTargets, max_num_moves) {
    BEINGS_TARGET_COUNTS = beingTargets;
    MAX_NUM_MOVES = max_num_moves;

    let statusBarContentDiv = document.createElement("div");
    statusBarContentDiv.setAttribute("id", "status-bar-content");

    const statusBar = document.getElementById("status-bar");
    statusBar.appendChild(statusBarContentDiv);

    setBeingsTargetBar(BEINGS_TARGET_COUNTS);
    setNumMovesBar(MAX_NUM_MOVES);
}


function render(nRows, nCols, beingTargets, maxNumMoves,
                initialGamePlayVars,
                clickCellEventHandler) {
    const randomCreaturesMap = getRandomCreaturesMap(nRows, nCols);

    // first initialize the map
    initializeMap(nRows, nCols);

    let board = document.getElementById("map");

    for (let i = 0; i < nRows; i++) {
        let row = board.children[i];

        // create a row html element
        for (let j = 0; j < nCols; j++) {
            let beingName = randomCreaturesMap[i][j];
            // get the cell
            let cell = row.children[j];
            setCellBeingInfo(cell, beingName);
        }
    }

    // initialize the gameplay variabels
    initialGamePlayVars(nRows, nCols);
    // set the event listeners
    setClickEventListeners(clickCellEventHandler);

    // initialize the game state
    setGameStateCanvas(beingTargets, maxNumMoves);
}

function redraw (creaturesMap,
                 beingTargets,
                 maxNumMoves,
                 initializeGamePlayVars,
                 clickCellEventHandler) {
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
    // make sure to set the global variables correctly
    initializeGamePlayVars(nRows, nCols);

    // set the listeners
    setClickEventListeners(clickCellEventHandler);
    // at this point everything is good
    return true;
}

// a function to clear the map
function clear_map() {
    let board = document.getElementById("map");
    // set the html
    board.innerHTML = "";
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

// functions to handle the game play
function getCoordinates(cell) {
    let y = parseInt(cell.dataset["y"]);
    let x = parseInt(cell.dataset["x"]);
    return Array.of(y, x);
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

// a function to extract any sequences including a certain cell
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

    // consider the horizontal direction: to the right
    let right_x = x;

    while ((right_x + 1 < maxX) &&
    (getCell(y, right_x + 1).getAttribute("data-being")) === beingName) {
        right_x += 1;
    }

    // to the left
    let left_x = x;

    while((left_x -1 >= 0) &&
    (getCell(y, left_x - 1).getAttribute("data-being")) === beingName) {
        left_x -= 1;
    }

    let clearedCellsCoordinates= [];

    // create an array to save the coordinates of the cell to be cleared
    if (right_x - left_x + 1 >= 3) {
        for (let i = left_x; i <= right_x; i++) {
            clearedCellsCoordinates.push([y, i]);
        }
    }

    if (down_y - up_y + 1 >= 3) {
        for(let i = up_y; i <= down_y; i++) {
            clearedCellsCoordinates.push([i, x]);
        }
    }

    return clearedCellsCoordinates;
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




function updateGameStateCanvas() {

}