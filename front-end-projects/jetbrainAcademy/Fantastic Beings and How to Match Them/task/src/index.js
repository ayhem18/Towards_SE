/*
* This script is used to automate the board creation
*/

function render_map(n_rows, n_cols) {
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

window.renderMap = render_map

// call the function to create the board
window.renderMap(5, 5)

// a function to clear the map
function clear_map() {
    let board = document.getElementById("map");
    // set the html
    board.innerHTML = "";
}

window.clearMap = clear_map;

let user_clear_map = confirm("clear the board ?")

if (user_clear_map){
    window.clearMap();
}





