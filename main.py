from fastapi import FastAPI  
from auth import router as auth_router  
from config import get_db_connection  
import time  
  
app = FastAPI()  
  
app.include_router(auth_router)  
  
@app.get("/")  
def read_root():  
    return {"message": "Welcome to the FastAPI security testing application!"}  
  
# SQL Injection Vulnerability  
@app.get("/search")  
async def search(query: str):  
    conn = get_db_connection()  
    cursor = conn.cursor()  
    cursor.execute(f"SELECT * FROM items WHERE name LIKE '%{query}%'")  
    results = cursor.fetchall()  
    conn.close()  
    return {"results": results}  
  
# Safe Search Endpoint  
@app.get("/safe-search")  
async def safe_search(query: str):  
    conn = get_db_connection()  
    cursor = conn.cursor()  
    cursor.execute("SELECT * FROM items WHERE name LIKE ?", (f"%{query}%",))  
    results = cursor.fetchall()  
    conn.close()  
    return {"results": results}  
  
# Denial of Service Vulnerability  
@app.get("/dos")  
async def dos():  
    while True:  
        pass  
  
# Safe Endpoint to Avoid DoS  
@app.get("/safe-dos")  
async def safe_dos():  
    time.sleep(0.1)  
    return {"message": "This is a safe endpoint to avoid DoS"}  