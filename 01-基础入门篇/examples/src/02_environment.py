"""
章节：02 - 环境搭建
文档：01-基础入门篇/Python入门/02-环境搭建.md
"""

import sys
from pathlib import Path


def example_01_basic() -> None:
    """示例1：环境验证"""
    print(f"Python 版本：{sys.version}")
    print(f"Python 路径：{sys.executable}")
    if sys.version_info >= (3, 11):
        print("✅ Python 版本符合要求（3.11+）")
    else:
        print("❌ Python 版本过低，请升级到 3.11+")


def example_02_level1() -> None:
    """示例2：层级1 - 单文件脚本"""
    print("创建 hello.py 文件")
    print("运行：uv run python hello.py")


def example_03_level2() -> None:
    """示例3：层级2 - 创建项目结构"""
    print("uv init my-project")
    print("cd my-project")
    print("uv run python main.py")


def example_04_level3() -> None:
    """示例4：层级3 - 添加依赖库"""
    print("uv add requests")
    print("uv run python main.py")


def example_05_level4() -> None:
    """示例5：层级4 - 虚拟环境管理"""
    print("uv venv")
    print("source .venv/bin/activate  # Linux/Mac")
    print(".venv\\Scripts\\activate     # Windows")


def example_06_level5() -> None:
    """示例6：层级5 - 多项目环境隔离"""
    print("uv python install 3.11")
    print("uv python install 3.12")
    print("uv python pin 3.11  # 项目A")


def example_practical() -> None:
    """综合应用：完整项目初始化流程"""
    project_name = "data-analysis-project"
    print(f"项目名称：{project_name}")
    print("\n项目结构：")
    print("  data-analysis-project/")
    print("  ├── pyproject.toml")
    print("  ├── src/")
    print("  │   └── main.py")
    print("  └── tests/")


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 02 - 环境搭建")
    print("=" * 60)

    example_01_basic()
    example_02_level1()
    example_03_level2()
    example_04_level3()
    example_05_level4()
    example_06_level5()
    example_practical()

    print("=" * 60)
    print("✅ 所有示例运行完成")


if __name__ == "__main__":
    main()
