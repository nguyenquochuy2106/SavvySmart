# database.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Kết nối tới Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

