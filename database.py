from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# SQLite Database
DATABASE_URL = os.environ.get('DB_PATH')

engine = create_engine(DATABASE_URL, echo=True)

# Create database tables
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency for database session
def get_db():
    with Session(engine) as session:
        yield session
