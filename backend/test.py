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


def signup2():
    import requests

    url2 = 'http://127.0.0.1:8000/upload'
    file = {'file': open('C:\\Users\\owo\\Documents\\uwu-chat-app-uwu\\anarchy-chat\\backend\\politics.png', 'rb')}

    response = requests.post(url2, files=file)
    return response.json()

print(signup2())