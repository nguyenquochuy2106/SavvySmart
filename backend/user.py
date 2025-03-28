from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.database import supabase
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import bcrypt
import uuid
import jwt

router = APIRouter()

# ✅ JWT Authentication Setup
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ✅ Generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ User Model
class User(BaseModel):
    username: str
    email: str
    password: str

# ✅ Login Model
class LoginRequest(BaseModel):
    email: str
    password: str

# ✅ Transaction Model
class Transaction(BaseModel):
    user_id: str
    card_id: str
    amount: float
    category: str
    transaction_type: str
    note: str
    created_at: datetime = datetime.utcnow()

# ✅ Card Model
class Card(BaseModel):
    user_id: str
    brand: str
    card_number: str

# ✅ User Service
class UserService:
    def __init__(self):
        self.supabase = supabase

    def get_user_by_email(self, email: str):
        response = self.supabase.from_("users").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None

    def get_user_by_username(self, username: str):
        response = self.supabase.from_("users").select("*").eq("username", username).execute()
        return response.data[0] if response.data else None
    
    def register_user(self, user):
        """Đăng ký tài khoản mới"""
        hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

        # Gửi yêu cầu đăng ký vào Supabase
        response = self.supabase.from_("users").insert({
            "id": str(uuid.uuid4()),
            "username": user.username,
            "email": user.email,
            "password": hashed_pw
        }).execute()

        return True  # Trả về True nếu đăng ký thành công




user_service = UserService()

# ✅ API - Register User
@router.post("/register")
async def register(user: User):
    # Kiểm tra email đã tồn tại
    if user_service.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Kiểm tra username đã tồn tại
    if user_service.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    # Tiến hành đăng ký
    success = user_service.register_user(user)


# ✅ API - Login User
@router.post("/login")
async def login(user: User):
    # Kiểm tra email và mật khẩu
    user_in_db = user_service.get_user_by_email(user.email)
    if not user_in_db or not bcrypt.checkpw(user.password.encode(), user_in_db["password"].encode()):
        raise HTTPException(status_code=400, detail="Invalid email or password")
