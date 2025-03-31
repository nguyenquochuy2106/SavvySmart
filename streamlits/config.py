from supabase import create_client

SUPABASE_URL = "https://wvattyjoisrgyrxpchkp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind2YXR0eWpvaXNyZ3lyeHBjaGtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjE4NDY4MiwiZXhwIjoyMDU3NzYwNjgyfQ.CdxDo43AQBmygF2r7Fq497JtdBAAzxwINuUqxVk8ezQ"

# Tạo kết nối Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_connection():
    """Kiểm tra kết nối với Supabase bằng cách lấy danh sách users"""
    try:
        response = supabase.table("users").select("*").limit(1).execute()
        print("✅ Kết nối Supabase thành công!", response)
    except Exception as e:
        print("❌ Lỗi kết nối Supabase:", e)

if __name__ == "__main__":
    test_connection()

