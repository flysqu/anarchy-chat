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

document.addEventListener("DOMContentLoaded", function() {
  loginForm = document.getElementById("loginForm");
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
  
    let username = document.getElementById("loginusername");
    let pin = document.getElementById("loginpassword");
  
    if (username.value == "" || pin.value == "") {
      alert("Ensure you input a value in both fields!");
    } else {
      // perform operation with form input

      const requestData = {
        username: username.value,
        pin: pin.value,
      };
      response = await makeRequest(requestData, "https://anarchy-chat.onrender.com/login")
      console.log(JSON.parse(response))

      console.log(
        `This form has a username of ${username.value} and password of ${pin.value}`
      );
      
      console.log(JSON.parse(response).authkey)
      document.cookie = `pin=${pin.value};`;
      document.cookie = `username=${username.value}`;
      document.cookie = `authkey=${JSON.parse(response).authkey};`;

      username.value = "";
      pin.value = "";

      window.location.href = "home.html"
    }
  });

  signupForm = document.getElementById("signupForm");
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    let username = document.getElementById("signupusername");
    let pin = document.getElementById("signuppassword");

    if (username.value == "" || pin.value == "") {
      alert("Ensure you input a value in both fields!");
    } else {
      // perform operation with form input

      const requestData = {
        username: username.value,
        pin: pin.value,
      };
      response = await makeRequest(requestData, "https://anarchy-chat.onrender.com/signup")
      console.log(response)

      console.log(
        `This form has a username of ${username.value} and password of ${pin.value}`
      );
      
      if (JSON.parse(response).status == "success") {alert("User is registered! You may now login")}

      username.value = "";
      pin.value = "";
    }
  });

  
});

