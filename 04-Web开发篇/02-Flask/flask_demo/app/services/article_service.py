"""文章服务"""

from app.extensions import db
from app.models.article import Article


class ArticleService:
    """文章服务"""

    @staticmethod
    def get_all(status: str | None = None) -> list[Article]:
        """获取所有文章"""
        query = Article.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Article.created_at.desc()).all()

    @staticmethod
    def get_by_id(article_id: int) -> Article | None:
        """获取单篇文章"""
        return Article.query.get(article_id)

    @staticmethod
    def create(
        title: str, content: str, author_id: int, status: str = "draft"
    ) -> Article:
        """创建文章"""
        article = Article(
            title=title,
            content=content,
            author_id=author_id,
            status=status,
        )
        db.session.add(article)
        db.session.commit()
        return article

    @staticmethod
    def update(article_id: int, **kwargs) -> Article | None:
        """更新文章"""
        article = Article.query.get(article_id)
        if not article:
            return None
        for key, value in kwargs.items():
            if hasattr(article, key):
                setattr(article, key, value)
        db.session.commit()
        return article

    @staticmethod
    def delete(article_id: int) -> bool:
        """删除文章"""
        article = Article.query.get(article_id)
        if not article:
            return False
        db.session.delete(article)
        db.session.commit()
        return True
