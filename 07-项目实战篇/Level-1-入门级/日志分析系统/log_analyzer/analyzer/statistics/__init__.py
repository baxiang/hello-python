"""统计分析"""

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import list
from ..parsers import LogEntry


class LogStatistics:
    """日志统计"""
    
    @staticmethod
    def count_by_level(entries: list[LogEntry]) -> dict:
        """按级别统计"""
        counter = Counter(e.level for e in entries)
        return dict(counter)
    
    @staticmethod
    def count_by_hour(entries: list[LogEntry]) -> dict:
        """按小时统计"""
        counter = Counter(e.timestamp.hour for e in entries)
        return dict(sorted(counter.items()))
    
    @staticmethod
    def count_by_day(entries: list[LogEntry]) -> dict:
        """按天统计"""
        counter = Counter(e.timestamp.date() for e in entries)
        return dict(sorted(counter.items()))
    
    @staticmethod
    def error_summary(entries: list[LogEntry]) -> list[dict]:
        """错误摘要"""
        errors = [e for e in entries if e.level in ("ERROR", "CRITICAL")]
        return [
            {"timestamp": e.timestamp, "message": e.message}
            for e in errors[:50]  # 最近50条
        ]
    
    @staticmethod
    def frequent_messages(entries: list[LogEntry], top: int = 10) -> dict:
        """高频消息"""
        counter = Counter(e.message for e in entries)
        return dict(counter.most_common(top))
    
    @staticmethod
    def time_range(entries: list[LogEntry]) -> dict:
        """时间范围"""
        if not entries:
            return {"start": None, "end": None}
        
        timestamps = [e.timestamp for e in entries]
        return {
            "start": min(timestamps),
            "end": max(timestamps),
            "duration": max(timestamps) - min(timestamps)
        }
    
    @staticmethod
    def full_report(entries: list[LogEntry]) -> dict:
        """完整报告"""
        return {
            "total": len(entries),
            "time_range": LogStatistics.time_range(entries),
            "by_level": LogStatistics.count_by_level(entries),
            "by_hour": LogStatistics.count_by_hour(entries),
            "errors": LogStatistics.error_summary(entries),
            "top_messages": LogStatistics.frequent_messages(entries)
        }