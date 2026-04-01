"""Pydantic 模型"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# 商品模型
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: Optional[int] = None
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# 分类模型
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# 订单模型
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    items: list[OrderItemBase]
    address: str


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    address: str
    created_at: datetime
    
    class Config:
        from_attributes = True