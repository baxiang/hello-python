"""命令行界面"""

import sys
from pathlib import Path
from .operations import FileOperations


def main():
    """主入口"""
    if len(sys.argv) < 3:
        print("用法: file-processor <命令> <目录> [参数]")
        print("命令: prefix, suffix, timestamp, organize, duplicates")
        sys.exit(1)
    
    command = sys.argv[1]
    directory = sys.argv[2]
    
    if not Path(directory).exists():
        print(f"目录不存在: {directory}")
        sys.exit(1)
    
    if command == "prefix":
        prefix = sys.argv[3] if len(sys.argv) > 3 else "new_"
        results = FileOperations.add_prefix(directory, prefix)
        for r in results:
            print(r)
    
    elif command == "suffix":
        suffix = sys.argv[3] if len(sys.argv) > 3 else "_processed"
        results = FileOperations.add_suffix(directory, suffix)
        for r in results:
            print(r)
    
    elif command == "timestamp":
        results = FileOperations.add_timestamp(directory)
        for r in results:
            print(r)
    
    elif command == "organize":
        mode = sys.argv[3] if len(sys.argv) > 3 else "extension"
        if mode == "extension":
            result = FileOperations.organize_by_extension(directory)
        else:
            result = FileOperations.organize_by_date(directory)
        for k, v in result.items():
            print(f"{k}: {v} 个文件")
    
    elif command == "duplicates":
        result = FileOperations.find_duplicates(directory)
        for size, files in result.items():
            print(f"大小 {size}: {len(files)} 个重复文件")
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()