/*
* This script is used to automate the board creation
*/


const beingTargetCounts = new Map();
beingTargetCounts.set("zouwu", 3);
beingTargetCounts.set("kelpie", 0);
// beingTargetCounts.set("swooping", 6);


function fRender(nRows, nCols) {
    return render(nRows, nCols,
        beingTargetCounts,
        5,
        initializeGamePlayVars2,
        GP2_clickCellEventHandler);
}

function fRedraw(creaturesMap) {
    return redraw(creaturesMap,
        beingTargetCounts,
        5,
        initializeGamePlayVars2,
        GP2_clickCellEventHandler);
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


