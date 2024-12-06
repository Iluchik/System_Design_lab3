from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from typing import Optional
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stud:stud@postgreDB/archdb")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
		db = SessionLocal()
		try:
			yield db
		finally:
			db.close()

# ==== Models =========================================================================================================

# ---- User -----------------------------------------------------------------------------------------------------------
class User_description(BaseModel):
	first_name: str
	last_name: str
	email: str
	password: str
	age: Optional[int] = None
	adress: Optional[str] = None
	phone: Optional[str] = None

class User(Base): # Это класс SQLAlchemy, тут используется Base, А НЕ BaseModel!!!
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String, unique=True)
	password = Column(String)
	age = Column(String, nullable=True)
	adress = Column(String, nullable=True)
	phone = Column(String, nullable=True)
	idx = Index("user_idx", id, email)

class User_response(User_description):
	id: int
	class Config:
		orm_mode=True
# ---------------------------------------------------------------------------------------------------------------------

# ---- Package --------------------------------------------------------------------------------------------------------
class Package_description(BaseModel):
	recipient_id: int
	package_weight: int
	package_dimensions: int
	package_descriptions: str

class Package(Base):
	__tablename__ = "packages"
	product_id = Column(Integer, primary_key=True)
	sender_id = Column(Integer, nullable=False)
	recipient_id = Column(Integer, nullable=False)
	package_weight = Column(Integer, nullable=True)
	package_dimensions = Column(Integer, nullable=True)
	package_descriptions = Column(String, nullable=True)
	idx = Index("package_idx", product_id, sender_id, recipient_id)

class Package_response(Package_description):
	product_id: int
	sender_id: int
	class Config:
		orm_mode=True
# ---------------------------------------------------------------------------------------------------------------------
	
# =====================================================================================================================

Base.metadata.create_all(bind=engine)