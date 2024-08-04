// let's build some object 

function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


function SomeObject(name, age) {
    this.name = capitalize(name);
    this.age = age;

    this.sayHi = function () {
        return `Hi !! My name is ${this.name}. I am ${age} years old `
    }
}


const o1 = new SomeObject("ali", 35)
const o2 = new SomeObject("Ammar", 25)

// console.log(o1.sayHi())
// console.log(o2.sayHi())

// console.log(Object.getPrototypeOf(o1))



class Shape {

    name;
    sides;
    sideLength;
    
    constructor(name, sides, sideLength) {
        // don't forget the  'this' keyword
        this.name=name;
        this.sides=sides;
        this.sideLength = sideLength;
    }

    calcPerimeter() {
        return this.sideLength * this.sides; 
    }
}

// // let's create some shapes
let tr1 = new Shape("triangle", 3, 3);
let sq1 = new Shape("square", 4, 5);

console.log(tr1.calcPerimeter());
console.log(sq1.calcPerimeter());

class Square extends Shape {
    constructor(sideLength) { 
        super("square", 4, sideLength);
    }

    calcArea() {
        return this.sideLength * this.sideLength;
    }

    flex() {
        return `I am a better square with a side length of ${this.sideLength}. My area is ${this.calcArea()}. My parameter is ${this.calcPerimeter()}`;
    }
}


const better_square = new Square(5);
console.log(better_square.flex());


