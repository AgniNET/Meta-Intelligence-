from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import json
from auth import hash_password, verify_password, create_access_token
from model import get_ai_response

app = FastAPI()

DB_FILE = "users_db.json"

# Data models
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PromptRequest(BaseModel):
    prompt: str

# Utility functions
def load_users():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Routes
@app.post("/register")
def register(user: UserRegister):
    users = load_users()
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    users.append({
        "email": user.email,
        "password": hash_password(user.password)
    })
    save_users(users)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    users = load_users()
    for u in users:
        if u["email"] == user.email and verify_password(user.password, u["password"]):
            token = create_access_token({"sub": user.email})
            return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/ask")
def ask_ai(request: PromptRequest):
    answer = get_ai_response(request.prompt)
    return {"response": answer}
