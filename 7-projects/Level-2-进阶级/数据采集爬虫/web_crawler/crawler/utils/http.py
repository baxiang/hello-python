"""HTTP 客户端"""

import time
import random
from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import config


class HttpClient:
    """HTTP 客户端"""
    
    def __init__(
        self,
        timeout: float | None = None,
        retry_times: int | None = None
    ):
        self.timeout = timeout or config.timeout
        self.session = self._create_session(retry_times)
    
    def _create_session(self, retry_times: int | None = None) -> requests.Session:
        """创建带重试的 Session"""
        session = requests.Session()
        
        retry = Retry(
            total=retry_times or config.retry_times,
            backoff_factor=config.retry_delay,
            status_forcelist=[500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def get(
        self,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        **kwargs
    ) -> requests.Response:
        """GET 请求"""
        final_headers = config.get_headers()
        if headers:
            final_headers.update(headers)
        
        proxies = {"http": config.proxy, "https": config.proxy} if config.proxy else None
        
        response = self.session.get(
            url,
            headers=final_headers,
            params=params,
            timeout=self.timeout,
            proxies=proxies,
            **kwargs
        )
        response.raise_for_status()
        
        # 随机延迟
        time.sleep(config.get_delay())
        
        return response
    
    def post(
        self,
        url: str,
        data: dict | None = None,
        json: dict | None = None,
        headers: dict | None = None,
        **kwargs
    ) -> requests.Response:
        """POST 请求"""
        final_headers = config.get_headers()
        if headers:
            final_headers.update(headers)
        
        proxies = {"http": config.proxy, "https": config.proxy} if config.proxy else None
        
        response = self.session.post(
            url,
            data=data,
            json=json,
            headers=final_headers,
            timeout=self.timeout,
            proxies=proxies,
            **kwargs
        )
        response.raise_for_status()
        
        time.sleep(config.get_delay())
        
        return response
    
    def close(self) -> None:
        """关闭连接"""
        self.session.close()