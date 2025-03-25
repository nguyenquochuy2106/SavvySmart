# routes/transactions.py
from fastapi import APIRouter, HTTPException
from database import supabase
from models import Transaction

router = APIRouter()

# Thêm giao dịch mới
@router.post("/transactions")
def add_transaction(transaction: Transaction):
    response = supabase.table("transactions").insert(transaction.dict(exclude={"id", "created_at"})).execute()
    return {"message": "Transaction added successfully", "transaction_id": response.data[0]["id"]}

# Lấy danh sách giao dịch của user
@router.get("/transactions/{user_id}")
def get_transactions(user_id: str):
    response = supabase.table("transactions").select("*").eq("user_id", user_id).execute()
    return {"transactions": response.data}

# Xóa giao dịch
@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: str):
    response = supabase.table("transactions").delete().eq("id", transaction_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}
