from fastapi import APIRouter, HTTPException
from backend.database.supabase import add_transaction, get_transactions, delete_transaction, search_transactions

router = APIRouter()

@router.post("/add")
def add_new_transaction(transaction: dict):
    """
    Add a new financial transaction.
    """
    result = add_transaction(transaction)
    if not result:
        raise HTTPException(status_code=400, detail="Transaction could not be added")
    return {"message": "Transaction added successfully", "transaction": result}

@router.get("/list")
def list_transactions(user_id: str):
    """
    Retrieve all transactions for a user.
    """
    transactions = get_transactions(user_id)
    return {"transactions": transactions}

@router.delete("/delete/{transaction_id}")
def remove_transaction(transaction_id: str):
    """
    Delete a transaction by its ID.
    """
    success = delete_transaction(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}

@router.get("/search")
def search_transaction(user_id: str, query: str):
    """
    Search transactions based on a query.
    """
    results = search_transactions(user_id, query)
    return {"transactions": results}
