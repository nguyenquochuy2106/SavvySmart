from fastapi import APIRouter, HTTPException
from backend.database.supaBaseServices import DatabaseService
from backend.ml.faceRecognitionServices import FaceRecognitionService
from pydantic import BaseModel, EmailStr, Field
from typing import List

router = APIRouter()

# 📌 Khởi tạo dịch vụ Database & Face Recognition
db_service = DatabaseService()
face_recognition = FaceRecognitionService()

# 📌 Pydantic Models
class UserProfileUpdate(BaseModel):
    user_id: str
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class TransactionCreate(BaseModel):
    user_id: str
    amount: float
    category: str
    description: str

# 📌 Authentication Service
class AuthService:
    @staticmethod
    def register(user_data: dict):
        image_base64 = user_data.get("image")
        if not image_base64:
            raise HTTPException(status_code=400, detail="Image is required")
        embedding = face_recognition.generate_embedding(image_base64)
        user_result = db_service.create_user(user_data["email"], user_data["password"], user_data["full_name"])
        db_service.update_user(user_result["user_id"], face_embedding=embedding)
        return {"message": "User registered successfully", "user_id": user_result["user_id"]}

    @staticmethod
    def login(user_data: dict):
        image_base64 = user_data.get("image")
        input_embedding = face_recognition.generate_embedding(image_base64)
        users = db_service.get_all_users()
        for user in users:
            if face_recognition.compare_embeddings(input_embedding, user.get("face_embedding")):
                return {"message": "Login successful", "user_id": user["id"], "email": user["email"]}
        raise HTTPException(status_code=401, detail="Face not recognized")

# 📌 Transaction Service
class TransactionService:
    @staticmethod
    def add_transaction(transaction: TransactionCreate):
        return db_service.add_transaction(transaction.user_id, transaction.amount, transaction.category, transaction.description)

    @staticmethod
    def list_transactions(user_id: str):
        return db_service.get_user_transactions(user_id)

    @staticmethod
    def delete_transaction(transaction_id: str):
        return db_service.delete_transaction(transaction_id)

    @staticmethod
    def search_transactions(user_id: str, query: str):
        return db_service.search_transactions(user_id, query)

# 📌 Analytics Service
class AnalyticsService:
    @staticmethod
    def get_financial_analytics(user_id: str):
        transactions = db_service.get_user_transactions(user_id)
        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found")
        category_summary = {}
        monthly_trend = {"income": {}, "expense": {}}
        for t in transactions:
            category_summary[t.get("category", "Other")] = category_summary.get(t.get("category", "Other"), 0) + t.get("amount", 0)
            date = t.get("date", "Unknown")[0:7]
            monthly_trend[t.get("type", "expense")][date] = monthly_trend[t.get("type", "expense")].get(date, 0) + t.get("amount", 0)
        return {"category_summary": category_summary, "monthly_trend": monthly_trend}

# 📌 User Service
class UserService:
    @staticmethod
    def get_profile(user_id: str):
        user = db_service.get_user(user_id)
        return {k: v for k, v in user.items() if k != "password"}

    @staticmethod
    def update_profile(updated_data: UserProfileUpdate):
        return db_service.update_user(updated_data.user_id, updated_data.dict(exclude={"user_id"}))

# 📌 API Routes
@router.post("/register")(AuthService.register)
@router.post("/login")(AuthService.login)
@router.post("/transactions/add")(TransactionService.add_transaction)
@router.get("/transactions/list")(TransactionService.list_transactions)
@router.delete("/transactions/delete/{transaction_id}")(TransactionService.delete_transaction)
@router.get("/transactions/search")(TransactionService.search_transactions)
@router.get("/analytics")(AnalyticsService.get_financial_analytics)
@router.get("/profile/{user_id}")(UserService.get_profile)
@router.put("/profile/update")(UserService.update_profile)
