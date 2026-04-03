"""爬虫核心"""

from typing import Generator
from .utils import HttpClient
from .parsers import HTMLParser, ParseResult
from .storage import DataStorage, SQLiteStorage
from .config import config


class Crawler:
    """网页爬虫"""
    
    def __init__(
        self,
        output_format: str = "json",
        use_db: bool = False
    ):
        self.client = HttpClient()
        self.storage = DataStorage()
        self.db = SQLiteStorage() if use_db else None
        self.output_format = output_format
    
    def fetch(self, url: str) -> str:
        """获取页面内容"""
        response = self.client.get(url)
        return response.text
    
    def parse(self, html: str) -> ParseResult:
        """解析页面"""
        parser = HTMLParser(html)
        return parser.parse()
    
    def crawl(self, url: str) -> dict:
        """爬取单个页面"""
        html = self.fetch(url)
        result = self.parse(html)
        
        data = {
            "url": url,
            "title": result.title,
            "text": result.text[:1000],  # 截取前1000字符
            "links": result.links[:20],  # 前20个链接
            "meta": result.meta
        }
        
        if self.db:
            self.db.save(url, result.title, result.text)
        
        return data
    
    def crawl_multiple(
        self, 
        urls: list[str]
    ) -> Generator[dict, None, None]:
        """爬取多个页面"""
        for url in urls:
            try:
                yield self.crawl(url)
            except Exception as e:
                print(f"爬取失败 {url}: {e}")
    
    def save(self, data: list[dict], filename: str) -> str:
        """保存数据"""
        if self.output_format == "json":
            return self.storage.save_json(data, filename)
        elif self.output_format == "csv":
            return self.storage.save_csv(data, filename)
        elif self.output_format == "jsonl":
            return self.storage.save_jsonl(data, filename)
        else:
            return self.storage.save_json(data, filename)
    
    def close(self) -> None:
        """关闭连接"""
        self.client.close()


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: crawler <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    crawler = Crawler()
    
    print(f"正在爬取: {url}")
    data = crawler.crawl(url)
    
    print(f"标题: {data['title']}")
    print(f"链接数: {len(data['links'])}")
    
    crawler.save([data], "output.json")
    print("已保存到 output.json")
    
    crawler.close()


if __name__ == "__main__":
    main()