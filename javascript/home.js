async function makeRequest(data, url) {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        });
        const responseBody = await response.text();
        return responseBody
    } catch (error) {
        console.error("Error:", error);
    }
}

async function refreshMessagebox() {
    try {
        const pin = getCookie("pin")
        const authkey = getCookie("authkey")
        console.log(authkey)

        const requestData = {
            pin: pin,
            authkey: authkey,
        };

        // Make the request to fetch messages
        console.log(requestData)
        const response = await makeRequest(requestData, "https://anarchy-chat.onrender.com/getmessages");
        
        // Parse the response (assuming it's a JSON string)
        const responseJson = JSON.parse(response);
        console.log(responseJson)

        const chatbox = document.getElementById("chatbox");

        // Clear the chatbox before updating
        chatbox.innerHTML = '';

        // Append each message to the chatbox
        responseJson.messages.forEach(element => {
            chatbox.innerHTML += generateMessageHtml(element);
        });

    } catch (error) {
        console.error("Error occurred:", error);
    }
}

// Poll the message box every 5 seconds
setInterval(refreshMessagebox, 2000);
refreshMessagebox()

function generateMessageHtml(responseJson) {
    const date = new Date(responseJson.timestamp * 1000)
    const messageHTML = `<div id="message">
                    <div id="flex-container">
                        <p id="user">${responseJson.username}</p>
                        <p id="timestamp">${date.toLocaleDateString()}</p>
                    </div>
                        <p id="text">${responseJson.content}</p>
                    </div>`
    return messageHTML
}

// https://stackoverflow.com/a/15724300
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const pin = getCookie("pin")
const authkey = getCookie("authkey")

const requestData = {
    pin: pin,
    authkey: authkey,
};

username = getCookie("username")
document.getElementById("username").textContent = `Logged in as ${username}`

document.addEventListener("DOMContentLoaded", function() {
    sendMessage = document.getElementById("messageForm");
    sendMessage.addEventListener("submit", async (e) => {
        e.preventDefault();
        const pin = getCookie("pin");
        const authkey = getCookie("authkey");
        const content = document.getElementById("messageFormInput").value;

        const requestData = {
            pin: pin,
            authkey: authkey,
            content: content,
        };

        response = makeRequest(requestData, "https://anarchy-chat.onrender.com/sendmessage").then(response => {
            const responseJson = JSON.parse(response)
            console.log(responseJson)
        });

    });
});