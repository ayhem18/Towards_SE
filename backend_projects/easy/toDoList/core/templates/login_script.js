const button = document.getElementById("submit")

const username_field = document.getElementById('username_input')
const password_field = document.getElementById('password')

function send_creds(event) {
    username = username_field.textContent
    password = password_field.textContent
    console.log(`${username}, ${password}`)

    body = JSON.stringify({"username": username, "password": password})

    // send the credentials to the server through the javascript api 

    
}

button.addEventListener("click", send_creds)
