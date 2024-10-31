import requests
import json

# Define the base URL of the FastAPI server
BASE_URL = "http://127.0.0.1:8000"  # Change this if the server is running on a different host/port

# Function to test the signup endpoint
def test_signup(username, pin):
    url = f"{BASE_URL}/signup"
    data = {
        "username": username,
        "pin": pin
    }
    response = requests.post(url, json=data)
    print("Signup Response:", response.json())
    return response.json()

# Function to test the login endpoint
def test_login(username, pin):
    url = f"{BASE_URL}/login"
    data = {
        "username": username,
        "pin": pin
    }
    response = requests.post(url, json=data)
    print("Login Response:", response.json())
    return response.json()

# Function to test the send message endpoint
def test_send_message(username, pin, authkey, content):
    url = f"{BASE_URL}/sendmessage"
    data = {
        "username": username,
        "pin": pin,
        "authkey": authkey,
        "content": content
    }
    response = requests.post(url, json=data)
    print("Send Message Response:", response.json())
    return response.json()

# Function to test the get messages endpoint
def test_get_messages(pin, authkey):
    url = f"{BASE_URL}/getmessages"
    data = {
        "pin": pin,
        "authkey": authkey
    }
    response = requests.post(url, json=data)
    print("Get Messages Response:", response.json())
    return response.json()

# Main test execution
if __name__ == "__main__":
    # Test parameters
    username = "testuser"
    pin = "123456"
    message_content = "Hello, this is a test message!"

    # Test signup
    signup_response = test_signup(username, pin)

    if signup_response['status'] == 'success':
        # Test login after signup
        login_response = test_login(username, pin)

        if login_response['status'] == 'success':
            # Retrieve authkey after login
            authkey = login_response['authkey']

            # Test sending a message
            test_send_message(username, pin, authkey, message_content)

            # Test getting messages
            test_get_messages(pin, authkey)
        else:
            print("Login failed:", login_response)
    else:
        print("Signup failed:", signup_response)
