"""辅助函数"""

import os


class Environment:
    """环境管理"""
    
    DEV = "development"
    STAGING = "staging"
    PROD = "production"
    
    def __init__(self, env: str = None):
        self.env = env or os.getenv("ENV", self.DEV)
    
    def is_dev(self) -> bool:
        return self.env == self.DEV
    
    def is_staging(self) -> bool:
        return self.env == self.STAGING
    
    def is_prod(self) -> bool:
        return self.env == self.PROD