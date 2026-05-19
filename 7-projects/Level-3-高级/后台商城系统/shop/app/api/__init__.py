"""API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core import get_db
from ..models.schemas import (
    ProductCreate, ProductResponse,
    CategoryCreate, CategoryResponse,
    OrderCreate, OrderResponse
)
from ..services import ProductService, CategoryService, OrderService

router = APIRouter()


# 商品路由
@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create(db, product)


@router.get("/products", response_model=list[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 10,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    return ProductService.get_list(db, skip, limit, category_id)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product


# 分类路由
@router.post("/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return CategoryService.create(db, category.name, category.description, category.parent_id)


@router.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all(db)


# 订单路由
@router.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, user_id: int, db: Session = Depends(get_db)):
    return OrderService.create(db, user_id, order.items, order.address)


@router.get("/orders", response_model=list[OrderResponse])
def get_orders(user_id: int, db: Session = Depends(get_db)):
    return OrderService.get_by_user(db, user_id)