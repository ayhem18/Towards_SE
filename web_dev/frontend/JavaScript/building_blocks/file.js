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


// 

let count = 0 // the number of times the button has been clicked on 

// let's define a function that will create a paragraph element, and display the number of times the buttom has been clicked

const paragraph = document.createElement("p")

function on_click_buttom() {
    count += 1;
    paragraph.textContent = "This button has been clicked on " + String(count) + " time" + (count === 1 ?  "" : "s");
    if (count == 1) {
        document.body.appendChild(paragraph);
    } 
}

// const bnt = document.querySelector("button");
// bnt.addEventListener("click", on_click_buttom);

// let original_button_text = "";
// const mouse_hover_button_text = "Mind Your bussiness, would you?"
// // let's create a functin that would change the text of the button whever the user hovers on it

// let first = True;
// function on_mouse_hover_button(event) {

//     document.body.style.backgroundColor = "green";
//     // if (first) {
//     //     original_button_text = bnt.textContent;
//     //     first = False;
//     // }
//     // bnt.textContent = mouse_hover_button_text;
// }

// bnt.addEventListener("mouseover", on_mouse_hover_button)
// // bnt.addEventListener("mouseout", () => {    document.body.style.backgroundColor = "white";})


// //  Adding a button whose text changes when clicking  

const machine_btn = document.querySelector("button")
let button_on = false;

const button_on_text = "The machine is On";
const button_off_text = "The machine is Off";

machine_btn.addEventListener("click", () => {console.log("Button cliked !!!"); 
                                            if (button_on) {                                                    
                                                machine_btn.textContent = button_off_text; button_on=false} 
                                            else {
                                                machine_btn.textContent = button_on_text;
                                                button_on = true;
                                            }
                                        }
                            )
