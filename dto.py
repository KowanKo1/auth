from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemResponse(BaseModel):
    id: int
    name: str

class TransactionResponse(BaseModel):
    id: int
    createdAt: datetime
    modifiedAt: datetime
    quantity: int
    transaction_type: str  # "in" or "out"
    timestamp: datetime
    account_email: str
    item: ItemResponse  # Include the item as a nested response
