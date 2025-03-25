# routes/auth.py
from fastapi import APIRouter, HTTPException
from backend.database import supabase
from backend.models import User
import bcrypt

router = APIRouter()

# Hàm băm mật khẩu
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Đăng ký user mới
@router.post("/register")
def register(user: User):
    # Kiểm tra user đã tồn tại chưa
    existing_user = supabase.table("users").select("id").eq("email", user.email).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash mật khẩu & tạo user
    user.password = hash_password(user.password)
    response = supabase.table("users").insert(user.dict(exclude={"id", "created_at"})).execute()
    return {"message": "User registered successfully", "user_id": response.data[0]["id"]}

# Đăng nhập
@router.post("/login")
def login(email: str, password: str):
    user = supabase.table("users").select("*").eq("email", email).execute()
    
    if not user.data:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    user = user.data[0]
    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful", "user_id": user["id"]}
