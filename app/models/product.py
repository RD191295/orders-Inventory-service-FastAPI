from app.db.base import Base
from sqlalchemy import Column, Integer, String


# Create a Python class that inherits from Base and defines table columns using Mapped.
class Product(Base):
    
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, nullable= False, unique= True)
    name = Column(String, nullable= False)
    price = Column(Integer, nullable= False)
    stock = Column(Integer, nullable= False)