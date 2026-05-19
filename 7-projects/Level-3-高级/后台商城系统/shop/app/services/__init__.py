"""商品服务"""

from sqlalchemy.orm import Session
from typing import Optional
from .models import Product, ProductCreate


class ProductService:
    """商品服务"""
    
    @staticmethod
    def create(db: Session, product: ProductCreate) -> Product:
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def get(db: Session, product_id: int) -> Product | None:
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_list(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        category_id: Optional[int] = None
    ) -> list[Product]:
        query = db.query(Product).filter(Product.is_active == True)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_stock(db: Session, product_id: int, quantity: int) -> bool:
        product = ProductService.get(db, product_id)
        if not product or product.stock < quantity:
            return False
        product.stock -= quantity
        db.commit()
        return True


class CategoryService:
    """分类服务"""
    
    @staticmethod
    def create(db: Session, name: str, description: str = None, parent_id: int = None):
        category = Category(name=name, description=description, parent_id=parent_id)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    
    @staticmethod
    def get_all(db: Session) -> list:
        return db.query(Category).all()


class OrderService:
    """订单服务"""
    
    @staticmethod
    def create(db: Session, user_id: int, items: list, address: str):
        order = Order(user_id=user_id, address=address)
        db.add(order)
        db.flush()
        
        total = 0
        for item in items:
            product = ProductService.get(db, item.product_id)
            if product and product.stock >= item.quantity:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price
                )
                db.add(order_item)
                total += product.price * item.quantity
                ProductService.update_stock(db, item.product_id, item.quantity)
        
        order.total_amount = total
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> list:
        return db.query(Order).filter(Order.user_id == user_id).all()


from .models import Category, Order, OrderItem