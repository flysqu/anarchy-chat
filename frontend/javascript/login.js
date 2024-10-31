async function makeRequest(data, url) {
  try {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Origin": "http://example.com"
        },
        body: JSON.stringify(data)
    });
    const responseBody = await response.text();
    return responseBody
  } catch (error) {
    console.error("Error:", error);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  loginForm = document.getElementById("loginForm");
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    let username = document.getElementById("loginusername");
    let pin = document.getElementById("loginpassword");

    if (username.value == "" || pin.value == "") {
      alert("Ensure you input a value in both fields!");
      return;
    } else if (pin.value.lenght == 6) {
      alert("The pin needs to be 6 digits");
      return;
    } else {
      // perform operation with form input

      const requestData = {
        username: username.value,
        pin: pin.value,
      };
      response = await makeRequest(requestData, "http://127.0.0.1:8000/login");
      console.log(JSON.parse(response));

      // handle errors
      if (JSON.parse(response).status) {
        if (JSON.parse(response).message == "Incorrect pin") {
          alert("Username or pin incorrect");
          return;
        }
        if (JSON.parse(response).message == "User not found") {
          alert("Username or pin incorrect");
          return;
        }
      }

      console.log(
        `This form has a username of ${username.value} and password of ${pin.value}`
      );

      console.log(JSON.parse(response).authkey);
      document.cookie = `pin=${pin.value};`;
      document.cookie = `username=${username.value}`;
      document.cookie = `authkey=${JSON.parse(response).authkey};`;

      username.value = "";
      pin.value = "";

      window.location.href = "home.html";
    }
  });

  async function uploadFile(username) {
    // Get the file from the input element
    const fileInput = document.getElementById("fileInput");
    const originalFile = fileInput.files[0];

    // Ensure a file is selected
    if (!originalFile) {
      alert("Please select a file first.");
      return;
    }

    // Rename the file by creating a new File object with the desired name
    const renamedFile = new File(
      [originalFile],
      "uwu.png".replace("uwu", username),
      { type: originalFile.type }
    );

    // Prepare the FormData object
    const formData = new FormData();
    formData.append("file", renamedFile);

    try {
      // Send the file using fetch
      const response = await fetch("http://127.0.0.1:8000/uploadpfp", {
        method: "POST",
        body: formData,
      });

      // Handle the response
      if (response.ok) {
        const result = await response.json();
        console.log("File uploaded successfully:", result);
      } else {
        console.error("File upload failed:", response.statusText);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  }

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
      response = await makeRequest(requestData, "http://127.0.0.1:8000/signup");

      await uploadFile(username.value);

      console.log(response);

      // handle errors
      if (JSON.parse(response).status) {
        if (JSON.parse(response).message == "Incorrect pin") {
          alert("Pin is not a valid number");
          return;
        }
        if (JSON.parse(response).message == "User not found") {
          alert("Username already taken");
          return;
        }
      } else {
        alert("User is registered! You may now login");
      }

      username.value = "";
      pin.value = "";
    }
  });
});
