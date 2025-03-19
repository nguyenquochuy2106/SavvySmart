from fastapi import APIRouter, HTTPException, Depends
from backend.database.supabase import create_user, get_user, login_user, get_user_transactions
from backend.ml.facenet import generate_embedding, compare_embeddings

router = APIRouter()

@router.post("/register")
def register_user(user_data: dict):
    """
    Register a new user with FaceID.
    Expects: { "email": "user@example.com", "password": "123456", "full_name": "John Doe", "image": "base64_encoded_image" }
    """
    image_base64 = user_data.get("image")
    if not image_base64:
        raise HTTPException(status_code=400, detail="Image is required for registration")

    # Convert image to embedding
    embedding = generate_embedding(image_base64)
    if embedding is None:
        raise HTTPException(status_code=400, detail="Failed to generate face embedding")

    # Create user in Supabase
    user_result = create_user(user_data["email"], user_data["password"], user_data["full_name"])
    if "error" in user_result:
        raise HTTPException(status_code=400, detail=user_result["error"])

    # Store embedding in Supabase under the user's record
    user_id = user_result["user_id"]
    update_result = get_user(user_id)
    if update_result:
        update_result["face_embedding"] = embedding
        return {"message": "User registered successfully", "user": update_result}
    else:
        raise HTTPException(status_code=500, detail="Failed to update user with face embedding")


@router.post("/login")
def login(user_data: dict):
    """
    Login with FaceID.
    Expects: { "image": "base64_encoded_image" }
    """
    image_base64 = user_data.get("image")
    if not image_base64:
        raise HTTPException(status_code=400, detail="Image is required for login")

    # Generate embedding from input image
    input_embedding = generate_embedding(image_base64)
    if input_embedding is None:
        raise HTTPException(status_code=400, detail="Failed to generate face embedding")

    # Get all users and compare embeddings
    users = get_user_transactions("")  # Fetch all users
    for user in users:
        stored_embedding = user.get("face_embedding")
        if stored_embedding and compare_embeddings(input_embedding, stored_embedding):
            return {"message": "Login successful", "user": user}

    raise HTTPException(status_code=401, detail="Face not recognized")
