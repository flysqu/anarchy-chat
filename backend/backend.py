from fastapi import FastAPI, Request, HTTPException, File, UploadFile
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import hashlib
import time
import random
import base64
from PIL import Image
import io

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST","OPTIONS"],
    allow_headers=["*"],
)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, pin TEXT, authkey TEXT, online TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (content TEXT, username TEXT, id TEXT, timestamp REAL)''')
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

class DeleteMessagesBody(BaseModel):
    pin: str
    authkey: str
    msgid: int

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

def convertToBase64(filename):
    with open(f"uploads\\pfp\\{filename}", "rb") as image2string: 
        converted_string = base64.b64encode(image2string.read()) 
    return converted_string 

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

@app.post("/uploadpfp")
async def upload(file: UploadFile = File(...)):
        contents = await file.read()
        
        # Check if the uploaded file is an image
        if "image" not in file.content_type:
            return {"status": "Error", "message": "The file attempted to upload is not an image"}
        
        # Check the file size (should be < 4MB)
        if len(contents) > 4000000:
            return {"status": "Error", "message": "The image is over 4MB in size, try something smaller :3"}
        
        # Open the image and resize it to 64x64 pixels
        image = Image.open(io.BytesIO(contents))
        image = image.resize((128, 128))
        
        # Save the downscaled image to the uploads directory
        downscaled_path = f"uploads/pfp/{file.filename}"
        image.save(downscaled_path)

        await file.close()

        return {"status": "Success", "message": f"Successfully uploaded and resized {file.filename}"}

@app.post("/signup")
async def signup(body: SignupBody):
    username = body.username
    pin = body.pin

    # Validate the pin (should be 6 digits)
    if not (pin.isdigit() and len(pin) == 6):
        return {"status": "error", "message": "Pin is not a valid number"}

    # Database connection
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
    cursor.execute("INSERT INTO users (name, pin, authkey, online) VALUES (?, ?, ?, ?)", 
                   (username, pin, authkey, "false"))
    conn.commit()
    conn.close()

    return {"status": "success", "authkey": authkey}


# Delete message
@app.post("/deletemessage")
async def deletemessage(body: DeleteMessagesBody):
    pin = body.pin
    authkey = get_authkey(pin)
    msgid = str(body.msgid)
    
    if authkey != body.authkey:
        return {"status": "error", "message": "Wrong pin or authkey"}

    conn = sqlite3.connect('app.db')
    conn.set_trace_callback(print)

    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages WHERE id = ?', (msgid,))
    
    conn.commit()
    conn.close()

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

    id = random.randint(0,999999)

    cursor.execute("INSERT INTO messages (content, username, timestamp, id) VALUES (?, ?, ?, ?)", (content, username, timestamp, id))
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

    return {"status": "success", "profilepics": [{"user": f"{filename.split(".")[0]}", "pfp": f"{convertToBase64(filename)}"} for filename in os.listdir("uploads\\pfp")], "messages": [{"content": msg[0], "username": msg[1], "id": msg[2], "timestamp": msg[3]} for msg in messages]}

# uvicorn script_name:app --reload
