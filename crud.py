from sqlmodel import Session, select
from models import Item, Category, Transaction, Account
from typing import Optional

# CRUD for user
def create_account(db: Session, account: Account) -> Account:
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_account_by_email(db:Session, email:str) -> Account:
    query = select(Account).where(Account.email == email)
    return db.exec(query).first()
