from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import SQLITE_DB_PATH


engine = create_engine(url = SQLITE_DB_PATH, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind = engine,autoflush=False, autocommit = False, expire_on_commit=False)

