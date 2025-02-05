from pydantic import BaseModel
from typing import List

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # ✅ Updated for Pydantic v2

class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # ✅ Updated for Pydantic v2
