# 项目三：博客 API 服务

> 掌握 FastAPI 和搜索功能

---

## 项目目标

- 掌握 FastAPI 框架
- 实现搜索功能
- 分页和排序
- API 文档

---

## 第一部分 - API 设计

```
博客 API
├── 文章
│   ├── GET /posts              # 文章列表
│   ├── GET /posts/{slug}       # 文章详情
│   ├── POST /posts             # 创建文章
│   ├── PUT /posts/{id}         # 更新文章
│   ├── DELETE /posts/{id}      # 删除文章
│   └── POST /posts/{id}/view   # 浏览文章
├── 分类
│   ├── GET /categories         # 分类列表
│   └── GET /categories/{slug} # 分类文章
├── 标签
│   ├── GET /tags               # 标签列表
│   └── GET /tags/{slug}/posts  # 标签文章
├── 评论
│   ├── GET /posts/{id}/comments
│   └── POST /posts/{id}/comments
└── 用户
    ├── POST /auth/register
    ├── POST /auth/login
    └── GET /users/me
```

---

## 第二部分 - 实现步骤

### 2.1 Pydantic 模型

```python
# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    is_published: bool = False


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    is_published: Optional[bool] = None


class TagResponse(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    summary: Optional[str]
    cover_image: Optional[str]
    view_count: int
    is_published: bool
    is_featured: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    author: dict
    category: Optional[CategoryResponse]
    tags: List[TagResponse]

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)
    parent_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: dict
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True
```

### 2.2 API 路由

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db, init_db
from models import Post, Category, Tag, Comment
from services import PostService, CategoryService, TagService
from schemas import (
    PostCreate, PostUpdate, PostResponse, PostListResponse,
    CategoryResponse, TagResponse,
    CommentCreate, CommentResponse
)

app = FastAPI(title="博客 API", version="1.0.0")


# 文章路由
@app.get("/posts", response_model=PostListResponse)
def get_posts(
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    sort_by: str = Query("published_at"),
    order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    """获取文章列表"""
    service = PostService(db)

    posts, total = service.get_published_posts(
        category_id=category_id,
        tag_id=tag_id,
        keyword=keyword,
        page=page,
        page_size=page_size
    )

    total_pages = (total + page_size - 1) // page_size

    return PostListResponse(
        items=posts,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@app.get("/posts/{slug}", response_model=PostResponse)
def get_post(slug: str, db: Session = Depends(get_db)):
    """获取文章详情"""
    service = PostService(db)
    post = service.get_post(slug=slug)

    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")

    if not post.is_published:
        raise HTTPException(status_code=403, detail="文章未发布")

    # 增加浏览量
    service.increment_view_count(post.id)

    return post


@app.post("/posts", response_model=PostResponse, status_code=201)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user = None  # 需要认证
):
    """创建文章"""
    service = PostService(db)

    # 实际应该从 current_user 获取作者 ID
    author_id = 1

    post = service.create_post(
        title=data.title,
        content=data.content,
        author_id=author_id,
        slug=data.slug if hasattr(data, 'slug') else None,
        summary=data.summary,
        cover_image=data.cover_image,
        category_id=data.category_id,
        tag_ids=data.tag_ids,
        is_published=data.is_published
    )

    return post


@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db)
):
    """更新文章"""
    service = PostService(db)

    update_data = data.model_dump(exclude_unset=True)
    post = service.update_post(post_id, **update_data)

    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")

    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """删除文章"""
    service = PostService(db)

    if not service.delete_post(post_id):
        raise HTTPException(status_code=404, detail="文章不存在")

    return {"message": "删除成功"}


@app.post("/posts/{post_id}/view")
def view_post(post_id: int, db: Session = Depends(get_db)):
    """浏览文章"""
    service = PostService(db)
    service.increment_view_count(post_id)
    return {"message": "浏览量已更新"}


# 分类路由
@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """获取分类列表"""
    service = CategoryService(db)
    return service.get_all_categories()


@app.get("/categories/{slug}/posts", response_model=PostListResponse)
def get_category_posts(
    slug: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取分类下的文章"""
    service = CategoryService(db)
    categories = service.get_all_categories()

    category = next((c for c in categories if c.slug == slug), None)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    post_service = PostService(db)
    posts, total = post_service.get_published_posts(
        category_id=category.id,
        page=page,
        page_size=page_size
    )

    return PostListResponse(
        items=posts,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


# 标签路由
@app.get("/tags", response_model=List[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    """获取标签列表"""
    service = TagService(db)
    return service.get_all_tags()


@app.get("/tags/popular")
def get_popular_tags(limit: int = Query(20, ge=1, le=50), db: Session = Depends(get_db)):
    """获取热门标签"""
    service = TagService(db)
    return service.get_popular_tags(limit)


# 评论路由
@app.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """获取文章评论"""
    comments = db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.parent_id == None,
        Comment.is_approved == True
    ).order_by(Comment.created_at.desc()).all()

    return comments


@app.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db)
):
    """创建评论"""
    # 检查文章是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")

    comment = Comment(
        post_id=post_id,
        author_id=1,  # 实际从认证获取
        content=data.content,
        parent_id=data.parent_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


# 健康检查
@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 第三部分 - 搜索功能

### 3.1 简单搜索

```python
# 使用 LIKE 查询
def search_posts(self, keyword: str, page: int = 1, page_size: int = 10):
    """搜索文章"""
    query = self.db.query(Post).filter(
        and_(
            Post.is_published == True,
            or_(
                Post.title.ilike(f"%{keyword}%"),
                Post.content.ilike(f"%{keyword}%"),
                Post.summary.ilike(f"%{keyword}%")
            )
        )
    )

    total = query.count()
    posts = query.order_by(Post.view_count.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return posts, total
```

### 3.2 高级搜索

```python
def advanced_search(
    self,
    keyword: str = None,
    category_id: int = None,
    tag_ids: List[int] = None,
    date_from: datetime = None,
    date_to: datetime = None,
    page: int = 1,
    page_size: int = 10
):
    """高级搜索"""
    query = self.db.query(Post).filter(Post.is_published == True)

    if keyword:
        query = query.filter(
            or_(
                Post.title.ilike(f"%{keyword}%"),
                Post.content.ilike(f"%{keyword}%")
            )
        )

    if category_id:
        query = query.filter(Post.category_id == category_id)

    if tag_ids:
        query = query.join(Post.tags).filter(Tag.id.in_(tag_ids))

    if date_from:
        query = query.filter(Post.published_at >= date_from)

    if date_to:
        query = query.filter(Post.published_at <= date_to)

    total = query.count()
    posts = query.order_by(Post.published_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return posts, total
```

---

## 第四部分 - 项目总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| FastAPI | Web 框架 |
| RESTful | API 设计 |
| 搜索 | 关键词搜索 |
| 分页 | 列表分页 |
| 排序 | 多种排序方式 |

### 下一步

在 [项目四](./04-内容管理系统.md) 中，我们将：
- 富文本编辑器
- 标签管理
- 分类管理
- 用户管理

---

[← 上一篇](./02-博客后端服务.md) | [下一篇 →](./04-内容管理系统.md)