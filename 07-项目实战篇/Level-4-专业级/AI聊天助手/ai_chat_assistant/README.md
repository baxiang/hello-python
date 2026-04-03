# AI 聊天助手

基于 LLM API 的智能对话应用，支持 CLI 和 Web 界面。

## 功能

- LLM API 对话
- 流式响应
- 对话历史管理
- CLI 命令行界面

## 安装

```bash
uv sync
```

## 运行

```bash
uv run ai-chat
```

## 配置

创建 `.env` 文件：

```
OPENAI_API_KEY=your-api-key
MODEL=gpt-4o-mini
```