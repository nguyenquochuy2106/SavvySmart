from supabase import create_client, Client
from backend.ml.facenet import generate_embedding, compare_embeddings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("https://wvattyjoisrgyrxpchkp.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind2YXR0eWpvaXNyZ3lyeHBjaGtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjE4NDY4MiwiZXhwIjoyMDU3NzYwNjgyfQ.CdxDo43AQBmygF2r7Fq497JtdBAAzxwINuUqxVk8ezQ")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in the .env file.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


### USER MANAGEMENT FUNCTIONS ###

# Create a new user
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in the .env file.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


### AUTHENTICATION FUNCTIONS ###

# Register a new user
def create_user(email: str, password: str, full_name: str):
    auth_response = supabase.auth.sign_up({"email": email, "password": password})
    if "error" in auth_response:
        return {"error": auth_response["error"]["message"]}
    
    user_id = auth_response["user"]["id"]
    user_data = {"id": user_id, "email": email, "full_name": full_name, "face_embedding": None}
    supabase.table("users").insert(user_data).execute()
    return {"message": "User registered successfully", "user_id": user_id}

# Login with email & password
# Login using FaceID
def login_user(image_base64: str):
    """
    Authenticate user using FaceID.
    Expects: Base64-encoded image.
    """
    input_embedding = generate_embedding(image_base64)
    if input_embedding is None:
        return {"error": "Failed to generate face embedding"}

    # Get all users with stored face embeddings
    response = supabase.table("users").select("id, email, full_name, face_embedding").execute()
    users = response.data if response.data else []

    # Compare embeddings to find a match
    for user in users:
        stored_embedding = user.get("face_embedding")
        if stored_embedding and compare_embeddings(input_embedding, stored_embedding):
            return {"message": "Login successful", "user": user}

    return {"error": "Face not recognized"}

# Get user details by user_id
def get_user(user_id: str):
    response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    return response.data if response.data else None

# Update user profile
def update_user(user_id: str, full_name: str = None, email: str = None):
    update_data = {}
    if full_name:
        update_data["full_name"] = full_name
    if email:
        update_data["email"] = email

    response = supabase.table("users").update(update_data).eq("id", user_id).execute()
    return {"message": "User updated successfully"} if response.data else {"error": "Failed to update user"}

# Get all transactions for a user
def get_user_transactions(user_id: str):
    response = supabase.table("transactions").select("*").eq("user_id", user_id).execute()
    return response.data if response.data else []


### TRANSACTION MANAGEMENT FUNCTIONS ###

# Add a transaction
def add_transaction(user_id: str, amount: float, category: str, description: str):
    transaction = {
        "user_id": user_id,
        "amount": amount,
        "category": category,
        "description": description
    }
    response = supabase.table("transactions").insert(transaction).execute()
    return response.data if response.data else {"error": "Failed to add transaction"}

# Get all transactions
def get_transactions():
    response = supabase.table("transactions").select("*").execute()
    return response.data if response.data else []

# Delete a transaction by ID
def delete_transaction(transaction_id: str):
    response = supabase.table("transactions").delete().eq("id", transaction_id).execute()
    return {"message": "Transaction deleted"} if response.data else {"error": "Failed to delete transaction"}

# Search transactions by keyword in description or category
def search_transactions(user_id: str, query: str):
    response = (
        supabase.table("transactions")
        .select("*")
        .eq("user_id", user_id)
        .or_(f"description.ilike.%{query}%,category.ilike.%{query}%")
        .execute()
    )
    return response.data if response.data else []

