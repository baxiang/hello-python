"""HTML 解析器"""

from bs4 import BeautifulSoup
from typing import Optional
from dataclasses import dataclass


@dataclass
class ParseResult:
    """解析结果"""
    title: str = ""
    links: list[dict] = None
    images: list[dict] = None
    text: str = ""
    meta: dict = None
    
    def __post_init__(self):
        if self.links is None:
            self.links = []
        if self.images is None:
            self.images = []
        if self.meta is None:
            self.meta = {}


class HTMLParser:
    """HTML 解析器"""
    
    def __init__(self, html: str, parser: str = "lxml"):
        self.soup = BeautifulSoup(html, parser)
    
    def parse(self) -> ParseResult:
        """解析页面"""
        return ParseResult(
            title=self.get_title(),
            links=self.get_links(),
            images=self.get_images(),
            text=self.get_text(),
            meta=self.get_meta()
        )
    
    def get_title(self) -> str:
        """获取标题"""
        title = self.soup.find("title")
        return title.text.strip() if title else ""
    
    def get_links(self) -> list[dict]:
        """获取所有链接"""
        links = []
        for a in self.soup.find_all("a", href=True):
            links.append({
                "text": a.text.strip(),
                "href": a["href"]
            })
        return links
    
    def get_images(self) -> list[dict]:
        """获取所有图片"""
        images = []
        for img in self.soup.find_all("img"):
            images.append({
                "src": img.get("src", ""),
                "alt": img.get("alt", "")
            })
        return images
    
    def get_text(self) -> str:
        """获取纯文本"""
        return self.soup.get_text(separator="\n", strip=True)
    
    def get_meta(self) -> dict:
        """获取 meta 信息"""
        meta = {}
        for tag in self.soup.find_all("meta"):
            name = tag.get("name") or tag.get("property", "")
            content = tag.get("content", "")
            if name and content:
                meta[name] = content
        return meta
    
    def select(self, selector: str) -> list:
        """CSS 选择器"""
        return self.soup.select(selector)
    
    def select_one(self, selector: str):
        """CSS 选择器（单个）"""
        return self.soup.select_one(selector)
    
    def find(self, tag: str, **attrs) -> Optional[BeautifulSoup]:
        """查找元素"""
        return self.soup.find(tag, attrs)
    
    def find_all(self, tag: str, **attrs) -> list:
        """查找所有元素"""
        return self.soup.find_all(tag, attrs)