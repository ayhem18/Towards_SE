// this is a script to run few lines of code
function checkTheDate(value){
    switch ((1 <= value) && (value <= 5)) {
        case true:
            console.log("Yes, you should go to work");
            break;
        default:
            console.log("No, this is your well-deserved weekend!");
    }
}

const planets = ["Earth", "Jupiter", "Neptune"];

function showPlanets(planets) {
    planets.forEach(function(v) {console.log(v);});
}

showPlanets(planets);

let firstStr = "Apple";
let secondStr = "Apple Iphone";

let compareTwo = secondStr.localeCompare(firstStr)
console.log(compareTwo);


let txt = "I slit the sheet, the sheet I slit, and on the slitted sheet I sit";
let searchStr = "sheet";

console.log(txt.search(searchStr));

function prepareData(line) {
    return line.trim().toLowerCase();
    //write your code here
}

console.log(prepareData("    Live has always been shit little mna..        "));


function speak(n) {
    let temp = "bark ".repeat(n)
    return temp.substring(0, temp.length - 1);
    //write your code here
}

let t = speak(3);
console.log(t.length);

function introduction(line) {
    let parts = line.split(" ")
    return parts[parts.length - 1];
}


console.log(introduction("Hello I am Ayhem"));
console.log(introduction("Hello I am Khalifa"));


function greeting(line) {
    let name = line.substring(0, 10).trim()
    let job = line.substring(21, line.length).trim();
    //write your code here
    return ("My name is " + name + " and I'm a " + job + ".");
}

console.log(greeting("Ayhemovich123456789  ML engineer"));