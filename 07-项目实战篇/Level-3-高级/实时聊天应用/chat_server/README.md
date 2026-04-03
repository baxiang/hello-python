# 实时聊天应用

基于 WebSocket 的多人实时聊天服务器。

## 功能

- WebSocket 实时通信
- 用户管理
- 消息存储
- REST API

## 安装

```bash
uv sync
```

## 运行

```bash
uv run uvicorn app.main:app --reload
```

## API

- `GET /api/users` - 获取在线用户
- `GET /api/messages` - 获取历史消息
- `WS /ws/{username}` - WebSocket 聊天