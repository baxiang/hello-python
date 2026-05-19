"""WebSocket任务通知"""

import json
from collections import defaultdict
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """WebSocket连接管理器"""

    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []
        self.rooms: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket) -> None:
        """接受新连接"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """断开连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        for room in self.rooms.values():
            if websocket in room:
                room.remove(websocket)

    async def send_personal_message(
        self, message: dict[str, Any], websocket: WebSocket
    ) -> None:
        """发送个人消息"""
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict[str, Any]) -> None:
        """广播消息给所有连接"""
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    async def connect_to_room(
        self, websocket: WebSocket, room: str
    ) -> None:
        """加入房间"""
        await websocket.accept()
        self.rooms[room].append(websocket)

    def leave_room(self, websocket: WebSocket, room: str) -> None:
        """离开房间"""
        if websocket in self.rooms[room]:
            self.rooms[room].remove(websocket)

    async def broadcast_to_room(
        self, message: dict[str, Any], room: str, sender: WebSocket
    ) -> None:
        """广播消息给房间内其他连接"""
        for connection in self.rooms[room]:
            if connection != sender:
                await connection.send_text(json.dumps(message))


manager = ConnectionManager()


async def task_websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket端点处理"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get("type") == "ping":
                    await manager.send_personal_message({"type": "pong"}, websocket)
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {"type": "error", "detail": "无效的JSON格式"},
                    websocket,
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def room_websocket_endpoint(websocket: WebSocket, room: str) -> None:
    """WebSocket房间端点处理"""
    await manager.connect_to_room(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                await manager.broadcast_to_room(message, room, websocket)
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {"type": "error", "detail": "无效的JSON格式"},
                    websocket,
                )
    except WebSocketDisconnect:
        manager.leave_room(websocket, room)


async def broadcast_task_event(event: str, task_id: int) -> None:
    """广播任务事件"""
    await manager.broadcast({"event": event, "task_id": task_id})
