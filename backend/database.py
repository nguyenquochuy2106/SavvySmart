from supabase import create_client, Client
import os
from typing import Optional, Dict, List
from passlib.context import CryptContext

# 📌 Kết nối Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL","https://wvattyjoisrgyrxpchkp.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind2YXR0eWpvaXNyZ3lyeHBjaGtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjE4NDY4MiwiZXhwIjoyMDU3NzYwNjgyfQ.CdxDo43AQBmygF2r7Fq497JtdBAAzxwINuUqxVk8ezQ")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DatabaseService:
    def __init__(self):
        self.client = supabase

    def create_user(self, email: str, password: str, full_name: str) -> Dict:
        hashed_password = pwd_context.hash(password)
        response = self.client.table("users").insert({
            "email": email,
            "password": hashed_password,
            "full_name": full_name
        }).execute()
        return response.data[0] if response.data else {}

    def get_user(self, user_id: str) -> Optional[Dict]:
        response = self.client.table("users").select("*").eq("id", user_id).single().execute()
        return response.data if response.data else None

    def update_user(self, user_id: str, update_data: Dict) -> Dict:
        response = self.client.table("users").update(update_data).eq("id", user_id).execute()
        return response.data[0] if response.data else {}

    def get_all_users(self) -> List[Dict]:
        response = self.client.table("users").select("*").execute()
        return response.data if response.data else []

    def add_transaction(self, user_id: str, amount: float, category: str, description: str) -> Dict:
        response = self.client.table("transactions").insert({
            "user_id": user_id,
            "amount": amount,
            "category": category,
            "description": description
        }).execute()
        return response.data[0] if response.data else {}

    def get_user_transactions(self, user_id: str) -> List[Dict]:
        response = self.client.table("transactions").select("*").eq("user_id", user_id).execute()
        return response.data if response.data else []

    def delete_transaction(self, transaction_id: str) -> Dict:
        response = self.client.table("transactions").delete().eq("id", transaction_id).execute()
        return response.data[0] if response.data else {}

    def search_transactions(self, user_id: str, query: str) -> List[Dict]:
        response = self.client.table("transactions").select("*").ilike("description", f"%{query}%").eq("user_id", user_id).execute()
        return response.data if response.data else []
