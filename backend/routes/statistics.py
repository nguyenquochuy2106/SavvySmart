from fastapi import APIRouter, HTTPException
from backend.database.supabase import get_user_transactions

router = APIRouter()

@router.get("/overview")
def get_financial_overview(user_id: str):
    """
    Get financial statistics for the user.
    """
    transactions = get_user_transactions(user_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }
