from fastapi import APIRouter, HTTPException, Form  
import time  
  
router = APIRouter()  
  
database = {  
    "users": {  
        "admin": "password123",  
        "user1": "user1password"  
    },  
    "messages": [  
        {"user": "admin", "message": "<script>alert('XSS')</script>"},  
        {"user": "user1", "message": "Hello, world!"}  
    ]  
}  
  
# Brute Force Vulnerability  
@router.post("/login")  
async def login(username: str = Form(...), password: str = Form(...)):  
    if username in database["users"] and database["users"][username] == password:  
        return {"message": "Login successful"}  
    else:  
        return {"message": "Login failed"}  
  
# Safe Login Endpoint  
@router.post("/safe-login")  
async def safe_login(username: str = Form(...), password: str = Form(...)):  
    if username in database["users"] and database["users"][username] == password:  
        return {"message": "Login successful"}  
    else:  
        time.sleep(1)  # Delay to prevent brute force  
        raise HTTPException(status_code=401, detail="Login failed")  
  
# XSS Vulnerability  
@router.post("/message")  
async def message(user: str = Form(...), message: str = Form(...)):  
    database["messages"].append({"user": user, "message": message})  
    return {"message": "Message added"}  
  
# Safe Message Endpoint  
@router.post("/safe-message")  
async def safe_message(user: str = Form(...), message: str = Form(...)):  
    safe_message = message.replace("<", "&lt;").replace(">", "&gt;")  
    database["messages"].append({"user": user, "message": safe_message})  
    return {"message": "Message added"}  