"""命令行界面"""

import sys
import json
from pathlib import Path
from .parsers import LogParser
from .statistics import LogStatistics


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("用法: log-analyzer <日志文件> [格式]")
        print("格式: python, apache, generic")
        sys.exit(1)
    
    filepath = sys.argv[1]
    format_type = sys.argv[2] if len(sys.argv) > 2 else "generic"
    
    if not Path(filepath).exists():
        print(f"文件不存在: {filepath}")
        sys.exit(1)
    
    # 解析日志
    parser = LogParser(format_type)
    entries = list(parser.parse_file(filepath))
    
    print(f"解析完成: {len(entries)} 条日志")
    
    # 统计分析
    report = LogStatistics.full_report(entries)
    
    # 输出报告
    print("\n=== 日志分析报告 ===")
    print(f"总条数: {report['total']}")
    print(f"时间范围: {report['time_range']['start']} - {report['time_range']['end']}")
    
    print("\n按级别统计:")
    for level, count in report["by_level"].items():
        print(f"  {level}: {count}")
    
    print("\n按小时统计:")
    for hour, count in report["by_hour"].items():
        print(f"  {hour:02d}时: {count}")
    
    print("\n高频消息:")
    for msg, count in report["top_messages"].items():
        print(f"  [{count}] {msg[:50]}...")
    
    # 保存报告
    output_file = Path(filepath).with_suffix(".report.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n报告已保存: {output_file}")


if __name__ == "__main__":
    main()