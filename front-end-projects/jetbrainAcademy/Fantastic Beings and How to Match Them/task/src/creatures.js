/*
* This script contains functionalities to manipulate the creatures data
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

function generateRandomBeingName() {
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
            matrix[i][j] = generateRandomBeingName();
        }
    }
    return matrix;
}

// set it as an attribute to the window object.
window.generateRandomBeingName = generateRandomBeingName;

