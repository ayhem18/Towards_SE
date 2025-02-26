// const fetchPromise = fetch(
// "https://mdn.github.io/learning-area/javascript/apis/fetching-data/can-store/products.json",
// );

// fetchPromise.then((response) => {
//     const jsonPromise = response.json();
//     jsonPromise.then((data) => {
//         console.log(data[2].name);
//     });
// });


// let's see what we can do with settimeout


// setTimeout((argument) => {console.log(argument)}, 55, "async 1: I am executed asyncronously");

// let j = 0;

// for (let i = 0; i <= 1000; i++) {
//     j++;
// }

// console.log(`sync 1:  ${j}`);

// console.log("sync 2: ");


// setTimeout(() => {
//     console.log("async 2: I am the 2nd function executed asyncronously");
// }, 50);

// console.log("sync 3: I am the third line of code");



// for (let number = 5; number < 9; number++) {
//     setTimeout(() => console.log(number), 5000 - number * 100);
// }

async function evenOrOdd(number) {
    let promise = new Promise((resolve, reject) => {
      if (number % 2 === 0) {
        setTimeout(() => resolve(number / 2), 1000);
      } else {
        setTimeout(() => reject(number * 2), 1000);
      }
    });
    return promise;
}


// for (let i = 0; i < 10; i++) {
//     evenOrOdd(i).then((result) => {
//         console.log(result);
//     }).catch((error) => {
//         console.log("an error was caught: ", error);
//     });
// }


function myFunc() {
    for (let i = 1; i < 6; i++) {
        // i to the power of 3
        console.log(i ** 3);    
    }
}

myFunc();
