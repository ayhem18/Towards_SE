// let select = document.querySelector("select");
// let para = document.querySelector("p");

// select.addEventListener("change", setWeather);

// function setWeather() {
//   const choice = select.value;

//   if (choice === "sunny") {
//     para.textContent =  
//       "It is nice and sunny outside today. Wear shorts! Go to the beach, or the park, and get an ice cream.";
//   } else if (choice === "rainy") {
//     para.textContent =
//       "Rain is falling outside; take a rain coat and an umbrella, and don't stay out for too long.";
//   } else if (choice === "snowing") {
//     para.textContent =
//       "The snow is coming down — it is freezing! Best to stay in with a cup of hot chocolate, or go build a snowman.";
//   } else if (choice === "overcast") {
//     para.textContent =
//       "It isn't raining, but the sky is grey and gloomy; it could turn any minute, so take a rain coat just in case.";
//   } else {
//     para.textContent = "";
//   }
// }


const names = ['Chris', 'Li Kang', 'Anne', 'Francesca', 'Mustafa', 'Tina', 'Bert', 'Jada'];
const para2 = document.createElement('p');

// Add your code here

function getRandomInt(min_int, max_int){
    return Math.floor(Math.random() * (max_int - min_int)) + min_int
}


function chooseName(array) {
    let index = getRandomInt(0, array.length - 1);
    return array[index];
}

// Don't edit the code below here!

section.innerHTML = ' ';
para2.textContent = chooseName(names)
section.appendChild(para2);


    