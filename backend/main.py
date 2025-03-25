# main.py
from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.cards import router as cards_router
from routes.transactions import router as transactions_router

app = FastAPI()

# Đăng ký các router
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(cards.router, prefix="/cards", tags=["Cards"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
def home():
    return {"message": "Welcome to SavvySave API"}
