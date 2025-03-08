/**
 * a simple javascript file to practice the theory about arrays. Just following the lectures 
 * from the hyperskill JavaScript Core Course !!!
 */


const a1 = new Array(1, 2, 3, 4, 5);

let global_variable = 0;

a1.forEach((element, index, array) => {
    global_variable += element;
    console.log(`the element at index ${index} is ${element} and the array is ${array}`);
});

// console.log(`the global variable is ${global_variable}`);


let animals = ["cat", "dog", "elephant"];
animals.forEach((animal, index, array) => {
    array[index] = animal.toUpperCase();
});
// console.log(animals); // ["CAT", "DOG", "ELEPHANT"]


let animalSlice = animals.slice(1, 3);

console.log(animalSlice);

animalSlice[0] = "bird";

// console.log(animalSlice);
// console.log(animals);



let arr = [4, 5, 8, 91, 45, 23, 0, 9, 4, 33];
arr.splice(4, 3, 2, 6);
// console.log(arr.length);


// animals.splice(1, 0, "bird", "fish");
// console.log(animals);

function removeTail(array) {
    let copy = array.slice();
    let n = copy.length;
    copy.splice(n - 2, 2, 0)
    return copy;
}

arr = Array(10).fill(1);
console.log(removeTail(arr));

numbers = ['1', '2', '3', '4', '5'];

console.log(numbers.map(number => Number(number)));
