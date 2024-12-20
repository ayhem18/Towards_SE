/**
 * This script is mainly about game Play: keeping track of the map, clearing and refilling
 */

// // a global variable to save the number of cleared cells in each column, row
// const CLEARED_BY_ROW = new Map();
// const CLEARED_BY_COLUMN = new Map();
// // a global variable saving the currently clicked cell
// let GP1_CLICKED_CELL = null;
//
// function initializeVars1(n_rows, n_cols) {
//     // after initializing the map, set the values in the CLEARED_BY_ROW and CLEARED_BY_COLUMN accordingly
//     // writing this piece of code in the initializeMap function ensures that those variables will be set correctly
//     // when redrawing the map
//     CLEARED_BY_ROW.clear();
//     CLEARED_BY_COLUMN.clear();
//
//     for (let i = 0; i < n_rows; i++) {
//         CLEARED_BY_ROW.set(i, 0)
//     }
//
//     for (let i = 0; i < n_cols; i++) {
//         CLEARED_BY_COLUMN.set(i, 0)
//     }
//
//     GP1_CLICKED_CELL = null;
// }
//
// function update_after_clearing_rows(rowIndex) {
//     // the idea here is to update the coordinates of each row with an index larger than the passed one
//     const board = document.getElementById("map");
//
//     // update the CLEARED_BY_ROW variable as follows:
//     // for each row larger than rowIndex, move the value CLEARED_BY_ROW[i] to the key i - 1
//     for (let i = rowIndex + 1; i < board.children.length; i++) {
//         CLEARED_BY_ROW.set(i - 1, CLEARED_BY_ROW.get(i));
//     }
//     // remove the last row
//     CLEARED_BY_ROW.delete(board.children.length - 1);
//
//     // decrement the number of cleared cells in each column
//     for (let i = 0; i < board.children[0].children.length; i++) {
//         CLEARED_BY_COLUMN.set(i, CLEARED_BY_COLUMN.get(i) - 1);
//     }
//
//     for (let i = rowIndex + 1; i < board.children.length; i++) {
//         for (let j = 0; j < board.children[i].children.length; j++) {
//             let cell = board.children[i].children[j];
//             // update the data-coords field for the cell element
//             cell.setAttribute("data-coords", `x${j}_y${i-1}`)
//
//             cell.setAttribute("data-x", `${j}`)
//             cell.setAttribute("data-y", `${i - 1}`)
//
//             // update the same attribute for the image if it exists (the cell might be cleared already)
//             if (cell.innerHTML !== "") {
//                 cell.children[0].setAttribute("data-coords", `y${j}_y${i-1}`);
//             }
//         }
//     }
//     // remove the <tr> element from the board
//     board.children[rowIndex].remove();
// }
//
// function update_after_clearing_columns(columnIndex) {
//     // the idea here is update all the columns
//     const board = document.getElementById("map");
//
//     // update the CLEARED_BY_COLUMN variable as follows
//     // for each row column larger than columnIndex, move the value CLEARED_BY_COLUMN[i] to the key i - 1
//     for (let i = columnIndex + 1; i < board.children[0].children.length; i++) {
//         CLEARED_BY_COLUMN.set(i - 1, CLEARED_BY_COLUMN.get(i));
//     }
//     CLEARED_BY_COLUMN.delete(board.children[0].children.length - 1);
//
//     // decrement the number of cleared cells in each row
//     for (let i = 0; i < board.children.length; i++) {
//         CLEARED_BY_ROW.set(i, CLEARED_BY_ROW.get(i) - 1);
//     }
//
//     for (let i = 0; i < board.children.length; i++) {
//         for (let j = columnIndex + 1; j < board.children[i].children.length; j++) {
//             let cell = board.children[i].children[j];
//             // update the data-coords field for the cell element
//             cell.setAttribute("data-coords", `x${j - 1}_y${i}`)
//
//             // make sure to update the "data-x" and "data-y" attributes
//             cell.setAttribute("data-x", `${j - 1}`)
//             cell.setAttribute("data-y", `${i}`)
//
//             // update the same attribute for the image if it exists (the cell might be cleared already)
//             if (cell.innerHTML !== "") {
//                 cell.children[0].setAttribute("data-coords", `y${j - 1}_y${i}`);
//             }
//         }
//         // remove the <td> cell completely from the dom
//         board.children[i].children[columnIndex].remove();
//     }
// }
//
// function clearCells(cellCoordinates) {
//
//     const board = document.getElementById("map");
//     let maxRows = board.children.length;
//     let maxCols = board.children[0].children.length;
//
//     for (let i = 0; i < cellCoordinates.length; i++) {
//         let y = cellCoordinates[i][0];
//         let x = cellCoordinates[i][1];
//         let cell = getCell(y, x);
//         // make sure to remove the image
//         cell.innerHTML = "";
//         // make sure to set the attribute to None, so it won't be used
//         cell.setAttribute("data-being", '');
//
//         // make sure to increase the number of cleared cells by row and column
//         // the column is determined by "x"
//         CLEARED_BY_COLUMN.set(x, CLEARED_BY_COLUMN.get(x) + 1);
//         CLEARED_BY_ROW.set(y, CLEARED_BY_ROW.get(y) + 1);
//     }
//
//     // make sure to start with later rows
//
//     for (let i = maxRows - 1; i >= 0; i--) {
//         if (CLEARED_BY_ROW.get(i) === maxRows) { // this means the i-th row has been fully cleared
//             // get the current coordinates
//             update_after_clearing_rows(i);
//         }
//     }
//
//     // make sure to start with later columns
//     for (let i = maxCols - 1; i >=0 ; i--) {
//         if (CLEARED_BY_COLUMN.get(i) === maxCols) { // this means the i-th row has been fully cleared
//             // get the current coordinates
//             update_after_clearing_columns(i);
//         }
//     }
// }
//
// function GP1ClickEventHandler(event) {
//     // step1: extract the event target
//     let targetCell = event.target;
//
//     // check if the target cell is an image element
//     if (targetCell.tagName.toLowerCase() === "img") {
//         targetCell = targetCell.parentNode;
//     }
//
//     if (targetCell.innerHTML === "") {
//         alert("An empty cell cannot be selected");
//         return;
//     }
//
//     // step2 proceed depending on the value of CLICKED_CELL
//     if (GP1_CLICKED_CELL === null) {
//         GP1_CLICKED_CELL = targetCell;
//         selectCell(targetCell);
//         return;
//     }
//
//     // at this point the CLICKED_CELL was set before the event
//     if (GP1_CLICKED_CELL === targetCell) {
//         // will be interpreted as deselecting the cell
//         deselectCell(targetCell);
//         GP1_CLICKED_CELL = null;
//         return;
//     }
//
//     // at this point the CLICKED_CELL is set and the target cell is different from CLICKED_CELL
//     // step1: make sure the cells are adjacent
//     // the coordinate attributes are saved at the image level and not the cell level (unfortunately)
//     if (! areCellsAdjacent(GP1_CLICKED_CELL, targetCell)) {
//         return;
//     }
//
//     swap(GP1_CLICKED_CELL, targetCell);
//     deselectCell(GP1_CLICKED_CELL);
//
//     // find whether the target cell is part of some sequence
//     let targetCoords = getCoordinates(targetCell);
//     let ty = targetCoords[0];
//     let tx = targetCoords[1];
//     let sequences1 = findSequences(ty, tx);
//
//
//     // find whether the clicked cell is part of some sequence
//     targetCoords = getCoordinates(GP1_CLICKED_CELL);
//     ty = targetCoords[0];
//     tx = targetCoords[1];
//     let sequences2 = findSequences(ty, tx)
//
//     // push all elements of the 2nd sequence to the first one
//     sequences1.push(...sequences2);
//
//     if (sequences1.length === 0) {
//         // swap the clicked and target cell back
//         // swap(CLICKED_CELL, targetCell);
//
//     } else {
//         // clear the sequences
//         clearCells(sequences1);
//     }
//
//     GP1_CLICKED_CELL = null;
// }
//
//
