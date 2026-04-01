"""文章服务"""

from sqlalchemy.orm import Session
from typing import Optional
from .models import Post, PostCreate, PostUpdate


class PostService:
    """文章服务"""
    
    @staticmethod
    def create(db: Session, post: PostCreate, author_id: int) -> Post:
        """创建文章"""
        db_post = Post(
            title=post.title,
            content=post.content,
            summary=post.summary,
            author_id=author_id
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    
    @staticmethod
    def get(db: Session, post_id: int) -> Post | None:
        """获取文章"""
        return db.query(Post).filter(Post.id == post_id).first()
    
    @staticmethod
    def get_list(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: Optional[int] = None
    ) -> list[Post]:
        """获取文章列表"""
        query = db.query(Post).filter(Post.is_published == True)
        if author_id:
            query = query.filter(Post.author_id == author_id)
        return query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, post_id: int, post: PostUpdate) -> Post | None:
        """更新文章"""
        db_post = PostService.get(db, post_id)
        if not db_post:
            return None
        
        update_data = post.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_post, key, value)
        
        db.commit()
        db.refresh(db_post)
        return db_post
    
    @staticmethod
    def delete(db: Session, post_id: int) -> bool:
        """删除文章"""
        db_post = PostService.get(db, post_id)
        if not db_post:
            return False
        
        db.delete(db_post)
        db.commit()
        return True
    
    @staticmethod
    def increment_view(db: Session, post_id: int) -> None:
        """增加浏览量"""
        db_post = PostService.get(db, post_id)
        if db_post:
            db_post.view_count += 1
            db.commit()