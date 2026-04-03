"""文件操作"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Callable


class FileOperations:
    """文件操作"""
    
    @staticmethod
    def rename_files(
        directory: str,
        pattern: Callable[[str], str],
        extensions: list[str] = None
    ) -> list[str]:
        """批量重命名"""
        dir_path = Path(directory)
        results = []
        
        for file in dir_path.iterdir():
            if file.is_file():
                if extensions and file.suffix.lower() not in extensions:
                    continue
                
                new_name = pattern(file.name)
                new_path = file.parent / new_name
                
                if new_path != file:
                    file.rename(new_path)
                    results.append(f"{file.name} -> {new_name}")
        
        return results
    
    @staticmethod
    def add_prefix(directory: str, prefix: str, extensions: list[str] = None) -> list[str]:
        """添加前缀"""
        return FileOperations.rename_files(
            directory,
            lambda name: f"{prefix}{name}",
            extensions
        )
    
    @staticmethod
    def add_suffix(directory: str, suffix: str, extensions: list[str] = None) -> list[str]:
        """添加后缀"""
        return FileOperations.rename_files(
            directory,
            lambda name: f"{Path(name).stem}{suffix}{Path(name).suffix}",
            extensions
        )
    
    @staticmethod
    def add_timestamp(directory: str, extensions: list[str] = None) -> list[str]:
        """添加时间戳"""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return FileOperations.rename_files(
            directory,
            lambda name: f"{Path(name).stem}_{ts}{Path(name).suffix}",
            extensions
        )
    
    @staticmethod
    def organize_by_extension(directory: str) -> dict:
        """按扩展名整理"""
        dir_path = Path(directory)
        result = {}
        
        for file in dir_path.iterdir():
            if file.is_file():
                ext = file.suffix.lower() or "no_extension"
                target_dir = dir_path / ext
                
                if not target_dir.exists():
                    target_dir.mkdir()
                
                target_path = target_dir / file.name
                shutil.move(str(file), str(target_path))
                
                result[ext] = result.get(ext, 0) + 1
        
        return result
    
    @staticmethod
    def organize_by_date(directory: str) -> dict:
        """按日期整理"""
        dir_path = Path(directory)
        result = {}
        
        for file in dir_path.iterdir():
            if file.is_file():
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                date_dir = mtime.strftime("%Y-%m")
                target_dir = dir_path / date_dir
                
                if not target_dir.exists():
                    target_dir.mkdir()
                
                target_path = target_dir / file.name
                shutil.move(str(file), str(target_path))
                
                result[date_dir] = result.get(date_dir, 0) + 1
        
        return result
    
    @staticmethod
    def delete_empty_dirs(directory: str) -> list[str]:
        """删除空目录"""
        dir_path = Path(directory)
        deleted = []
        
        for folder in sorted(dir_path.rglob("*"), reverse=True):
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
                deleted.append(str(folder))
        
        return deleted
    
    @staticmethod
    def find_duplicates(directory: str) -> dict:
        """查找重复文件"""
        dir_path = Path(directory)
        size_map = {}
        
        for file in dir_path.rglob("*"):
            if file.is_file():
                size = file.stat().st_size
                if size not in size_map:
                    size_map[size] = []
                size_map[size].append(str(file))
        
        return {k: v for k, v in size_map.items() if len(v) > 1}