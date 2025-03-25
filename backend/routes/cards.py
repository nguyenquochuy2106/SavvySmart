# routes/cards.py
from fastapi import APIRouter, HTTPException
from backend.database import supabase
from backend.models import Card

router = APIRouter()

# Thêm thẻ mới
@router.post("/cards")
def add_card(card: Card):
    response = supabase.table("cards").insert(card.dict(exclude={"id", "created_at"})).execute()
    return {"message": "Card added successfully", "card_id": response.data[0]["id"]}

# Lấy danh sách thẻ của user
@router.get("/cards/{user_id}")
def get_cards(user_id: str):
    response = supabase.table("cards").select("*").eq("user_id", user_id).execute()
    return {"cards": response.data}

# Xóa thẻ
@router.delete("/cards/{card_id}")
def delete_card(card_id: str):
    response = supabase.table("cards").delete().eq("id", card_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Card deleted successfully"}
