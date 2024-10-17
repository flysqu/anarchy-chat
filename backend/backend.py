from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import hashlib
import time

# Initialize FastAPI app
app = FastAPI()

# Define allowed origins (frontend URLs that should be allowed to call the API)
origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8001/home.html?",
    "https://anarchy-chat-lern.onrender.com/"
]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from listed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers, including Content-Type
)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, pin TEXT, authkey TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (content TEXT, username TEXT, timestamp REAL)''')
    conn.commit()
    conn.close()

init_db()

# Pydantic models for request bodies
class LoginBody(BaseModel):
    username: str
    pin: str

class SignupBody(BaseModel):
    username: str
    pin: str

class SendMessageBody(BaseModel):
    pin: str
    authkey: str
    content: str

class GetMessagesBody(BaseModel):
    pin: str
    authkey: str

# Helper function to get hashed pin
def get_authkey(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()

def get_username_from_pin(pin: str) -> str:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE pin = ?", (pin,))
    result = cursor.fetchone()
    conn.close

    return result

# Login endpoint
@app.post("/login")
async def login(body: LoginBody):
    username = body.username
    pin = body.pin
    authkey = get_authkey(pin)

    # Check if user exists
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        db_pin = result[1]
        if pin == db_pin:
            return {"status": "success", "authkey": authkey}
        else:
            return {"status": "error", "message": "Incorrect pin"}
    else:
        return {"status": "error", "message": "User not found"}

# Signup endpoint
@app.post("/signup")
async def signup(body: SignupBody):
    username = body.username
    pin = body.pin

    if not (pin.isdigit() and len(pin) == 6):
        return {"status": "error", "message": "Pin is not a valid number"}

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return {"status": "error", "message": "Username already taken"}

    # Create authkey
    authkey = get_authkey(pin)

    # Add user to database
    cursor.execute("INSERT INTO users (name, pin, authkey) VALUES (?, ?, ?)", (username, pin, authkey))
    conn.commit()
    conn.close()

    return {"status": "success", "authkey": authkey}

# Send message endpoint
@app.post("/sendmessage")
async def sendmessage(body: SendMessageBody):
    pin = body.pin
    authkey = get_authkey(pin)

    if authkey != body.authkey:
        return {"status": "error", "message": "Wrong pin or authkey"}

    username = get_username_from_pin(pin)[0]
    print(username)

    content = body.content
    timestamp = time.time()

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content, username, timestamp) VALUES (?, ?, ?)", (content, username, timestamp))
    conn.commit()
    conn.close()

    return {"status": "success", "message": "Message sent"}

# Get messages endpoint
@app.post("/getmessages")
async def getmessages(body: GetMessagesBody):
    pin = body.pin
    authkey = get_authkey(pin)

    if authkey != body.authkey:
        return {"status": "error", "message": "Wrong pin or authkey"}

    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    conn.close()

    return {"status": "success", "messages": [{"content": msg[0], "username": msg[1], "timestamp": msg[2]} for msg in messages]}

# uvicorn script_name:app --reload
