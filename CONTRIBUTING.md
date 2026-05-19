# 参与贡献

## 项目结构

```
hello-python/
├── 1-basics/          # 基础入门（Python 简介、语法、字符串、数据结构）
├── 2-core/            # 核心编程（函数、面向对象、异常、迭代器、装饰器、类型提示）
├── 3-advanced/        # 高级语法（模块与包、标准库、并发与异步）
├── 4-web/             # Web 开发（HTTP、Flask、FastAPI、认证、部署）
├── 5-ml/              # 机器学习（数据预处理、监督学习、无监督学习）
├── 6-deep-learning/   # 深度学习（神经网络、PyTorch、CNN、RNN）
├── 7-projects/        # 项目实战（从入门工具到完整系统）
├── 8-engineering/     # 工程实践（包管理、代码质量、测试、文档、运维）
├── 9-langchain/       # LangChain 与 LangGraph（LLM 应用开发）
├── appendix/          # 附录（环境配置、代码规范）
├── docs/              # 内部文档
└── scripts/           # 脚本工具
```

## 章节代码

每个章节（除 7-projects/ 外）都包含独立的 Python 项目。

```bash
cd 1-basics/01-Python入门
python main.py                    # 运行示例
python -m pytest                  # 运行测试
```

## 验证命令

```bash
./scripts/verify-code.sh             # 验证所有章节代码
./scripts/check-links.sh             # 检查链接有效性
```

## 代码风格

- Python 3.11+ 类型提示
- 遵循 PEP 8 规范
- 使用 ruff 进行代码检查
- 示例文件使用 `# ✅` 和 `# ❌` 标注
