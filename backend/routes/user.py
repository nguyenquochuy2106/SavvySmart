from fastapi import APIRouter, HTTPException
from backend.database.supabase import get_user, update_user

router = APIRouter()

@router.get("/profile/{user_id}")
def get_user_profile(user_id: str):
    """
    Retrieve user profile information.
    """
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}

@router.put("/profile/update")
def update_user_profile(user_id: str, updated_data: dict):
    """
    Update user profile information.
    """
    success = update_user(user_id, updated_data)
    if not success:
        raise HTTPException(status_code=400, detail="Profile update failed")
    return {"message": "Profile updated successfully"}
