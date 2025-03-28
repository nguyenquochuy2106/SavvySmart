from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.user import router as user_router

# ✅ Khởi tạo FastAPI app
app = FastAPI()

# ✅ Cấu hình CORS (Cho phép frontend gọi API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Chỉ định domain cụ thể nếu cần (VD: ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Đăng ký router từ user.py
app.include_router(user_router)

# ✅ Trang chủ kiểm tra API đang chạy
@app.get("/")
async def root():
    return {"message": "SavvySave API is running!"}

# ✅ Chạy server (Dùng lệnh: `uvicorn main:app --reload` trong terminal)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
