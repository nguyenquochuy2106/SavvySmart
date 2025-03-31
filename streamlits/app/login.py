import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from streamlits.services.auth_service import AuthService, FaceIDService

# Khởi tạo dịch vụ
auth_service = AuthService()
faceid_service = FaceIDService()

def main():
    st.set_page_config(page_title="SavvySmart Login", page_icon="🔐", layout="centered")
    st.title("🔐 SavvySmart - Đăng nhập")
    
    tab1, tab2 = st.tabs(["📧 Login", "📷 Face ID Login"])
    
    with tab1:
        st.subheader("Đăng nhập bằng Email & Mật khẩu")
        email = st.text_input("Email", placeholder="Nhập email")
        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")
        
        if st.button("Đăng nhập"):
            result = auth_service.login_user(email, password)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Chào mừng {result['user']['username']}!")
                st.session_state["user"] = result["user"]
                st.experimental_rerun()
    
    with tab2:
        st.subheader("Đăng nhập bằng Face ID")
        if st.button("Sử dụng Camera"):
            user_id = st.session_state.get("user", {}).get("id", None)
            if user_id:
                result = faceid_service.login_with_faceid(user_id)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Xác thực thành công! Chào mừng bạn.")
                    st.experimental_rerun()
            else:
                st.warning("Vui lòng đăng nhập bằng email trước để nhận diện khuôn mặt!")
    
    st.markdown("Chưa có tài khoản? [Đăng ký ngay](#)")

if __name__ == "__main__":
    main()