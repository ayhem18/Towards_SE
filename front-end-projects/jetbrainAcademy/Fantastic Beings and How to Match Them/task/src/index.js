/*
* This script is used to automate the board creation
*/


function fRender(nRows, nCols) {
    return render(nRows, nCols, initializeGamePlayVars2, GP2_clickCellEventHandler);
}

function fRedraw(creaturesMap) {
    return redraw(creaturesMap, initializeGamePlayVars2, GP2_clickCellEventHandler);
}

window.renderMap = fRender;

window.redrawMap = fRedraw;

window.clearMap = clear_map;

// call the function to create the board
window.renderMap(5, 5);

// window.redrawMap(
//     [['puffskein', 'swooping', 'swooping'],
//     ['kelpie', 'puffskein', 'puffskein'],
//     ['puffskein', 'kelpie', 'swooping'],
//     ['puffskein', 'zouwu', 'zouwu'],
//     ]
// )


