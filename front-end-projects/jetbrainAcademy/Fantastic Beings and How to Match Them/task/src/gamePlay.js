/**
 * This script is mainly about game Play: keeping track of the map, clearing and refilling
 */

// a global variable saving the currently clicked cell
let GP2_CLICKED_CELL = null;

function initializeGamePlayVars2(nRows, nCols) {
    // this game Play does not save any global information using the number of columns and rows
    GP2_CLICKED_CELL = null;
}

function clearCells(cellCoordinates) {
    for (let i = 0; i < cellCoordinates.length; i++) {
        let y = cellCoordinates[i][0];
        let x = cellCoordinates[i][1];
        let cell = getCell(y, x);
        // make sure to remove the image
        cell.innerHTML = "";
        // make sure to set the attribute to None, so it won't be used
        cell.setAttribute("data-being", '');
    }

}

function initialRefill(clearedCellsCoordinates) {
    for (let i = 0; i < clearedCellsCoordinates.length; i++) {
        let y = clearedCellsCoordinates[i][0];
        let x = clearedCellsCoordinates[i][1];
        let cell = getCell(y, x);

        // get a random being
        let beingName = window.generateRandomBeingName();
        // set the being related info.

        if (cell.innerHTML !== "") {
            throw `trying to fill a non-cleared cell. found inner HTML: ${cell.innerHTML}`
        }

        setCellBeingInfo(cell, beingName); // the image as well as the "data-being" attribute should be set
    }
}


function GP2_clickCellEventHandler(event) {
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
    if (GP2_CLICKED_CELL === null) {
        GP2_CLICKED_CELL = targetCell;
        selectCell(targetCell);
        return;
    }

    // at this point the CLICKED_CELL was set before the event
    if (GP2_CLICKED_CELL === targetCell) {
        // will be interpreted as deselecting the cell
        deselectCell(targetCell);
        GP2_CLICKED_CELL = null;
        return;
    }

    // at this point the CLICKED_CELL is set and the target cell is different from CLICKED_CELL
    // step1: make sure the cells are adjacent
    // the coordinate attributes are saved at the image level and not the cell level (unfortunately)
    if (! areCellsAdjacent(GP2_CLICKED_CELL, targetCell)) {
        return;
    }

    swap(GP2_CLICKED_CELL, targetCell);
    deselectCell(GP2_CLICKED_CELL);

    // find whether the target cell is part of some sequence
    let targetCoords = getCoordinates(targetCell);
    let ty = targetCoords[0];
    let tx = targetCoords[1];
    let sequences1 = findSequences(ty, tx);


    // find whether the clicked cell is part of some sequence
    targetCoords = getCoordinates(GP2_CLICKED_CELL);
    ty = targetCoords[0];
    tx = targetCoords[1];
    let sequences2 = findSequences(ty, tx)

    // push all elements of the 2nd sequence to the first one
    sequences1.push(...sequences2);

    // convert the elements to strings and filter by creating a set
    // make it an array
    // extract the two elements from the array and convert them back to integers
    sequences1 = Array.from(
                    new Set(sequences1.map((x) => `${x[0]}_${x[1]}`))
                    ).map(
                        (x) => x.split("_").map(x => parseInt(x))
                    );


    if (sequences1.length === 0) {
        // swap the clicked and target cell back
        swap(GP2_CLICKED_CELL, targetCell);
    } else {
        // clear the sequences
        clearCells(sequences1);
        initialRefill(sequences1);
    }

    GP2_CLICKED_CELL = null;
}


