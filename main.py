# main.py
from fastapi import FastAPI
from backend.routes import auth, cards, transactions

app = FastAPI()

# Đăng ký các router
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(cards.router, prefix="/cards", tags=["Cards"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
def home():
    return {"message": "Welcome to SavvySave API"}
