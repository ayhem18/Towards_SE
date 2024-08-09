let items_list = []; // an array to save the name of the list 

// main_section = document.querySelector("main");

// create the list element
const items_list_node = document.createElement("ul");

// styling the element with the "shop_list" class style...
// items_list_node.classList.add("shop_list"); (not necessarily apparently)

// create a function to add the elements to the list
function add_item(event) {
    // prevent sending the data
    event.preventDefault();
    
    // get the value from the 
    item = document.getElementById("item_text");
    item_name = item.value

    // log the item value anyway
    // console.log(`the passed item is: ${item_name}`);

    if (item_name == "") {
        alert("Can't keep the item");
        // console.log("The item has no name...");
        return;
    }

    items_list.push(item_name);
    // console.log(`The current length of the list is: ${items_list.length}`);    

    // create the list item
    let list_item = document.createElement("li");
    
    let text_node = document.createTextNode(item_name)
    // create a textNode to hold the text passed by the user 
    list_item.appendChild(text_node)

    // create a node to hold the butotn
    const item_button = document.createElement("button")
    item_button.textContent = "delete";
    // add the class for styling
    item_button.classList.add("list_button");

    list_item.appendChild(item_button);
    // // the attribute associated with 
    // list_item.innerText = item_name;

    if (items_list.length == 1) {
        document.body.appendChild(items_list_node);
    }

    items_list_node.appendChild(list_item);

    // set the text field to an empty string once again
    item.value = "";
}

// add the lister to the submit button
const submit_button = document.getElementById("submit_item")
submit_button.addEventListener("click", add_item)


// create a function at the list level: using the even bubbling te

function delete_item(event) {
    // find the button
    let list_item = event.target.parentElement;
    // the parent element should be the <li> element in the shopping list
    // remove it from the DOM as well as the list
    list_item.remove();
    items_list.remove(list_item);
}

items_list_node.addEventListener("click", delete_item);
