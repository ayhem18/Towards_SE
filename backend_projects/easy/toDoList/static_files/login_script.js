const button = document.getElementById("submit")

const username_field = document.getElementById('username_input')
const password_field = document.getElementById('pwd')

function send_creds(event) {

event.preventDefault();
username = username_field.textContent;
password = password_field.value;
console.log(`${username}, ${password}`);

body = JSON.stringify({"username": username, "password": password});

// send the credentials to the server through the javascript api 

fetch("2dl/authenticate/", {
	method: "POST",
	body: body,
	headers: {
		// according to this post on stack overflow: https://stackoverflow.com/questions/58308688/postman-post-method-using-raw-body-returns-500 
		// if I want to use the django standard way of buildings apis, I need to pass
		// http object with Content-type: multipart/form-data
		"Content-type": "multipart/form-data; charset=UTF-8"
	}
	}); 
}

button.addEventListener("click", send_creds)
