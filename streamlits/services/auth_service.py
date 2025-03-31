from config import supabase
import bcrypt
import cv2
import face_recognition
import numpy as np
import streamlit as st
import tempfile

class AuthService:
    def register_user(self, username: str, email: str, password: str, image_url: str):
        """Đăng ký người dùng mới"""
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        response = supabase.table("users").insert({
            "username": username,
            "email": email,
            "password": hashed_password,
            "image_url": image_url
        }).execute()
        return response

    def login_user(self, email: str, password: str):
        """Đăng nhập người dùng"""
        response = supabase.table("users").select("password, id, username, image_url").eq("email", email).execute()
        if not response.data:
            return {"error": "Email không tồn tại!"}
        
        user = response.data[0]
        if not bcrypt.checkpw(password.encode(), user["password"].encode()):
            return {"error": "Mật khẩu không đúng!"}
        
        return {"success": True, "user": user}

    def get_user_by_id(self, user_id: str):
        """Lấy thông tin người dùng theo ID"""
        response = supabase.table("users").select("username, email, image_url").eq("id", user_id).execute()
        return response.data[0] if response.data else None

class FaceIDService:
    def encode_face(self, image_path: str):
        """Mã hóa khuôn mặt từ ảnh"""
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        return encodings[0] if encodings else None

    def verify_face(self, input_image_path: str, stored_image_path: str):
        """So sánh khuôn mặt nhập vào với ảnh đã lưu"""
        input_encoding = self.encode_face(input_image_path)
        stored_encoding = self.encode_face(stored_image_path)
        
        if input_encoding is None or stored_encoding is None:
            return {"error": "Không nhận diện được khuôn mặt!"}
        
        result = face_recognition.compare_faces([stored_encoding], input_encoding)
        return {"success": result[0]}

    def capture_face(self):
        """Chụp ảnh từ webcam và lưu vào file tạm"""
        st.write("Vui lòng nhìn vào camera...")
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return None
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        cv2.imwrite(temp_file.name, frame)
        return temp_file.name

    def login_with_faceid(self, user_id: str):
        """Đăng nhập bằng Face ID"""
        user = supabase.table("users").select("image_url").eq("id", user_id).execute().data[0]
        if not user or "image_url" not in user:
            return {"error": "Không tìm thấy ảnh khuôn mặt!"}
        
        input_image = self.capture_face()
        if not input_image:
            return {"error": "Không thể chụp ảnh!"}
        
        return self.verify_face(input_image, user["image_url"])
