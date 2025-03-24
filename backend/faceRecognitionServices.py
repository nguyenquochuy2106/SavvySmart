from fastapi import APIRouter, HTTPException
from backend.database import DatabaseService
from pydantic import BaseModel, EmailStr, Field
from typing import List
from keras_facenet import FaceNet
from mtcnn import MTCNN
import numpy as np
import cv2

router = APIRouter()
db_service = DatabaseService()

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
        self.facenet_model = FaceNet()
        self.mtcnn_detector = MTCNN()

    def _detect_face(self, image):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        detections = self.mtcnn_detector.detect_faces(img_rgb)
        if not detections:
            return None
        x, y, width, height = detections[0]["box"]
        x, y = max(0, x), max(0, y)
        face = img_rgb[y:y+height, x:x+width]
        if face.shape[0] < 10 or face.shape[1] < 10:
            return None  
        face_resized = cv2.resize(face, (160, 160), interpolation=cv2.INTER_LINEAR)
        return face_resized.astype("float32") / 255.0

    def generate_embedding(self, image):
        face_array = self._detect_face(image)
        if face_array is None:
            return None
        face_array = np.expand_dims(face_array, axis=0)
        return self.facenet_model.embeddings(face_array)[0].tolist()

    def compare_embeddings(self, embedding1, embedding2, threshold=0.6):
        distance = np.linalg.norm(np.array(embedding1) - np.array(embedding2))
        return distance < threshold

face_recognition = FaceRecognitionService()

# 📌 Authentication Service
class AuthService:
    @staticmethod
    def register(user_data: dict):
        image_base64 = user_data.get("image")
        if not image_base64:
            raise HTTPException(status_code=400, detail="Image is required")
        embedding = face_recognition.generate_embedding(image_base64)
        user_result = db_service.create_user(user_data["email"], user_data["password"], user_data["full_name"])
        db_service.update_user(user_result["id"], {"face_embedding": embedding})
        return {"message": "User registered successfully", "user_id": user_result["id"]}

    @staticmethod
    def login(user_data: dict):
        image_base64 = user_data.get("image")
        input_embedding = face_recognition.generate_embedding(image_base64)
        users = db_service.get_all_users()
        for user in users:
            if face_recognition.compare_embeddings(input_embedding, user.get("face_embedding")):
                return {"message": "Login successful", "user_id": user["id"], "email": user["email"]}
        raise HTTPException(status_code=401, detail="Face not recognized")
