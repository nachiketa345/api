from fastapi import FastAPI
from backend.routers import accounts, users  # Import your users router

app = FastAPI()

# Include your routers
app.include_router(users.router)
app.include_router(accounts.router)  # Include the accounts router


@app.get("/")
def read_root():
    return {"message": "Welcome to the Bank API"}