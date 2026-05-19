"""WebSocket 路由"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from ..services import manager, store
from ..models import MessageType, UserStatus

router = APIRouter()


@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """WebSocket 聊天端点"""
    # 连接
    success = await manager.connect(websocket, username)
    
    if not success:
        await websocket.close(code=4000, reason="用户名已存在")
        return
    
    # 发送历史消息
    history = store.get_recent(50)
    await manager.send_to(username, {
        "type": MessageType.HISTORY.value,
        "messages": history
    })
    
    # 广播用户加入
    await manager.broadcast({
        "type": MessageType.JOIN.value,
        "username": username,
        "users": manager.get_users()
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            msg_type = message.get("type", "message")
            
            if msg_type == "message":
                content = message.get("content", "")
                
                # 保存消息
                store.save(username, content)
                
                # 广播消息
                await manager.broadcast({
                    "type": MessageType.MESSAGE.value,
                    "username": username,
                    "content": content
                })
            
            elif msg_type == "status":
                status = UserStatus(message.get("status", "online"))
                manager.set_status(username, status)
                await manager.broadcast({
                    "type": MessageType.STATUS.value,
                    "username": username,
                    "status": status.value
                })
    
    except WebSocketDisconnect:
        manager.disconnect(username)
        store.save(username, "离开了聊天", "system")
        
        await manager.broadcast({
            "type": MessageType.LEAVE.value,
            "username": username,
            "users": manager.get_users()
        })