async function makeRequest(data, url) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const responseBody = await response.text();
    return responseBody;
  } catch (error) {
    console.error("Error:", error);
  }
}

async function refreshMessagebox() {
  if (!document.hidden) {
    try {
      // update online value

      const pin = getCookie("pin");
      const authkey = getCookie("authkey");
      const username = getCookie("username");
      console.log(authkey);

      const requestData = {
        pin: pin,
        authkey: authkey,
      };

      // Make the request to fetch messages
      console.log(requestData);
      const response = await makeRequest(
        requestData,
        "http://127.0.0.1:8000/getmessages"
      );

      // Parse the response (assuming it's a JSON string)
      const responseJson = JSON.parse(response);
      console.log(responseJson);

      const chatbox = document.getElementById("chatbox");
      const profilepics = responseJson.profilepics;

      // Clear the chatbox before updating
      chatbox.innerHTML = "";

      // Append each message to the chatbox
      responseJson.messages.forEach((element) => {
        chatbox.innerHTML += generateMessageHtml(
          element,
          profilepics,
          username
        );
      });
    } catch (error) {
      const requestData = {
        pin: pin,
        authkey: authkey,
      };
      makeRequest(requestData, "http://127.0.0.1:8000/getmessages");
    }
  } else {
    // update online value
  }
}

setInterval(refreshMessagebox, 2000);
refreshMessagebox();

function generateMessageHtml(responseJson, profilepics, username) {
  const date = new Date(responseJson.timestamp * 1000);
  var messageHTML = ``;
  console.log(profilepics);
  var relevantProfilePic = ""

  profilepics.forEach((i) => {
    if (i.user == responseJson.username) {
        relevantProfilePic = i.pfp;
        console.log(relevantProfilePic)
    }
  });
  // if the message is sent by you
  if (responseJson.username == username) {
    messageHTML = `<div id="message">
                                    <div id="flex-container">
                                        <img id="pfp" src="data:image/jpeg;base64,${relevantProfilePic.replace("b'").slice(0, -1).replace("undefined","")}">
                                        <p id="user">${responseJson.username}</p>
                                        <p id="timestamp">${date.toLocaleDateString()}</p>
                                        <button id="deleteMsg" onclick="deleteMsg(${responseJson.id})">Delete</button>
                                    </div>
                                        <p id="text">${responseJson.content}</p>
                                    </div>`;
  } else {
    // sent by someone else
    messageHTML = `<div id="message">
                                    <div id="flex-container">
                                        <img id="pfp" src="data:image/jpeg;base64,${relevantProfilePic.replace("b'").slice(0, -1).replace("undefined","")}">
                                        <p id="user">${responseJson.username}</p>
                                        <p id="timestamp">${date.toLocaleDateString()} ${date.toLocaleTimeString()}</p>
                                    </div>
                                        <p id="text">${responseJson.content}</p>
                                    </div>`;
  }

  return messageHTML;
}

function deleteMsg(id) {
  const pin = getCookie("pin");
  const authkey = getCookie("authkey");

  const requestData = {
    pin: pin,
    authkey: authkey,
    msgid: id,
  };

  response = makeRequest(requestData, "http://127.0.0.1:8000/deletemessage").then((response) => {
    refreshMessagebox()
  });
}

// https://stackoverflow.com/a/15724300
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

const pin = getCookie("pin");
const authkey = getCookie("authkey");

const requestData = {
  pin: pin,
  authkey: authkey,
};

document.addEventListener("DOMContentLoaded", function () {
  username = getCookie("username");
  document.getElementById("username").textContent = `Logged in as ${username}`;
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

    response = makeRequest(
      requestData,
      "http://127.0.0.1:8000/sendmessage"
    ).then((response) => {
      refreshMessagebox()
      document.getElementById("messageFormInput").value = "" 
    });

  });
});
