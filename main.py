from fastapi import FastAPI
from database import init_db
from routes import accounts, categories, items, transactions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Inventory Management API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routes
app.include_router(accounts.router, prefix="/authentication", tags=["Authentication"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Inventory Management API"}
