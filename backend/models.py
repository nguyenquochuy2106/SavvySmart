# models.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Model
class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    password: str
    created_at: Optional[datetime] = None

# Card Model
class Card(BaseModel):
    id: Optional[str] = None
    user_id: str
    brand: str
    last_4_digits: str
    created_at: Optional[datetime] = None

# Transaction Model
class Transaction(BaseModel):
    id: Optional[str] = None
    user_id: str
    card_id: Optional[str] = None
    amount: float
    category: str
    transaction_type: str  # 'income' hoặc 'expense'
    note: Optional[str] = None
    created_at: Optional[datetime] = None
