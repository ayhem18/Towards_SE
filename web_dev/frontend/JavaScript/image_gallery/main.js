const displayedImage = document.querySelector('.displayed-img');
const thumbBar = document.querySelector('.thumb-bar');

const btn = document.querySelector('button');
const overlay = document.querySelector('.overlay');

/* Declaring the array of image filenames */
img_paths = ['images/pic1.jpg', 'images/pic2.jpg', 'images/pic3.jpg', 'images/pic4.jpg', 'images/pic5.jpg'];

/* Declaring the alternative text for each image file */
alt_texts = ["human eye", "looks like a pavement", "synthetic flowes", "wow", "butterfly"];

/* Looping through images */

let num_images = img_paths.length;

// 

function display_on_click(event) {
    displayedImage.setAttribute('src', event.target.src);
    displayedImage.setAttribute('alt', event.target.alt);
}


for (let i = 0; i < num_images; i++) {
    let newImage = document.createElement('img');
    newImage.setAttribute('src', img_paths[i]);
    newImage.setAttribute('alt', alt_texts[i]);
    thumbBar.appendChild(newImage);
}


/* Wiring up the Darken/Lighten button */
thumbBar.addEventListener("click", display_on_click);

// a boolean flag to know whether the image is darkened or not
let darken_mode = false;

function on_click_buttom() {
    console.log("clicked !!!")
    if (darken_mode) {
        darken_mode = false;
        // set the background opacity to 0.5
        overlay.style.backgroundColor = `rgb(0, 0, 0, 0)`
    }
    else{
        darken_mode = true;
        overlay.style.backgroundColor = `rgb(0, 0, 0, 0.5)`
    }
}

btn.addEventListener("click", on_click_buttom)
