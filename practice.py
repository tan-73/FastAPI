from fastapi import FastAPI, Depends, HTTPException, status, Security
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "your_secret_key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token["exp"] >= datetime.utcnow().timestamp():
            return decoded_token
        else:
            return None
    except jwt.PyJWTError:
        return None

app = FastAPI()

users_db = {
    "tanmay": {"username": "tanmay", "password": "12345", "role": "admin"}
}

class Login(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(user: Login):
    db_user = users_db.get(user.username)
    if not db_user or db_user['password'] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token_data = {"sub": user.username, "role": db_user.get("role", "user")}
    token = create_jwt_token(data=token_data)
    return {"access_token": token}

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return payload

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['sub']}! You are authenticated"}

@app.get("/admin")
async def admin_route(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
    return {"message": "Welcome, admin!"}

#practice