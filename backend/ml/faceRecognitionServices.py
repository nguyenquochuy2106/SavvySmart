from fastapi import APIRouter, HTTPException
from backend.database.supabase import (
    create_user, get_user, update_user, get_all_users,
    add_transaction, get_user_transactions, delete_transaction, search_transactions,
    get_budget_data, update_budget
)
from backend.ml.facenet import FaceRecognitionService
from pydantic import BaseModel, EmailStr, Field
from typing import List

router = APIRouter()

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

# 📌 Face Recognition Service
class FaceRecognitionService:
    def __init__(self):
        from keras_facenet import FaceNet
        from mtcnn import MTCNN
        from backend.ml.utils import preprocess_image
        import numpy as np
        import cv2
        
        self.facenet_model = FaceNet()
        self.mtcnn_detector = MTCNN()
        self.preprocess_image = preprocess_image
        
    def _detect_face(self, image_base64: str):
        img_array = self.preprocess_image(image_base64)
        if img_array is None:
            return None
        img_bgr = (img_array * 255).astype(np.uint8)
        img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2BGR)
        detections = self.mtcnn_detector.detect_faces(img_bgr)
        if len(detections) == 0:
            return None
        x, y, width, height = detections[0]["box"]
        x, y = max(0, x), max(0, y)
        face = img_bgr[y:y+height, x:x+width]
        if face.shape[0] < 10 or face.shape[1] < 10:
            return None  
        face_resized = cv2.resize(face, (160, 160), interpolation=cv2.INTER_LINEAR)
        return face_resized.astype("float32") / 255.0
    
    def generate_embedding(self, image_base64: str):
        face_array = self._detect_face(image_base64)
        if face_array is None:
            return None
        face_array = np.expand_dims(face_array, axis=0)
        return self.facenet_model.embeddings(face_array)[0].tolist()
    
    def compare_embeddings(self, embedding1, embedding2, threshold=0.6):
        import numpy as np
        distance = np.linalg.norm(np.array(embedding1) - np.array(embedding2))
        return distance < threshold

# 📌 Authentication Service
class AuthService:
    face_recognition = FaceRecognitionService()

    @staticmethod
    def register(user_data: dict):
        image_base64 = user_data.get("image")
        if not image_base64:
            raise HTTPException(status_code=400, detail="Image is required")
        embedding = AuthService.face_recognition.generate_embedding(image_base64)
        user_result = create_user(user_data["email"], user_data["password"], user_data["full_name"])
        update_user(user_result["user_id"], face_embedding=embedding)
        return {"message": "User registered successfully", "user_id": user_result["user_id"]}

    @staticmethod
    def login(user_data: dict):
        image_base64 = user_data.get("image")
        input_embedding = AuthService.face_recognition.generate_embedding(image_base64)
        users = get_all_users()
        for user in users:
            if AuthService.face_recognition.compare_embeddings(input_embedding, user.get("face_embedding")):
                return {"message": "Login successful", "user_id": user["id"], "email": user["email"]}
        raise HTTPException(status_code=401, detail="Face not recognized")

# 📌 Transaction Service
class TransactionService:
    @staticmethod
    def add_transaction(transaction: TransactionCreate):
        return add_transaction(transaction.user_id, transaction.amount, transaction.category, transaction.description)

    @staticmethod
    def list_transactions(user_id: str):
        return get_user_transactions(user_id)

    @staticmethod
    def delete_transaction(transaction_id: str):
        return delete_transaction(transaction_id)

    @staticmethod
    def search_transactions(user_id: str, query: str):
        return search_transactions(user_id, query)

# 📌 Analytics Service
class AnalyticsService:
    @staticmethod
    def get_financial_analytics(user_id: str):
        transactions = get_user_transactions(user_id)
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
        user = get_user(user_id)
        return {k: v for k, v in user.items() if k != "password"}

    @staticmethod
    def update_profile(updated_data: UserProfileUpdate):
        return update_user(updated_data.user_id, updated_data.dict(exclude={"user_id"}))

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