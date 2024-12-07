from fastapi import FastAPI
from database import init_db
from routes import accounts, items

app = FastAPI(title="Inventory Management API")

# Initialize database
init_db()

# Include routes
app.include_router(accounts.router, prefix="/authentication", tags=["Authentication"])
app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Inventory Management API"}
