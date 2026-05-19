"""WebSocket测试"""

import json

from fastapi.testclient import TestClient


class TestWebSocket:
    """WebSocket连接测试"""

    def test_websocket_connect(self, client: TestClient) -> None:
        """测试WebSocket连接"""
        with client.websocket_connect("/api/ws/tasks") as websocket:
            websocket.send_text(json.dumps({"type": "ping"}))
            data = websocket.receive_text()
            response = json.loads(data)
            assert response["type"] == "pong"

    def test_websocket_invalid_json(self, client: TestClient) -> None:
        """测试无效JSON"""
        with client.websocket_connect("/api/ws/tasks") as websocket:
            websocket.send_text("not json")
            data = websocket.receive_text()
            response = json.loads(data)
            assert response["type"] == "error"

    def test_ws_broadcast(self, client: TestClient) -> None:
        """测试WebSocket房间广播"""
        import time

        with (
            client.websocket_connect("/api/ws/rooms/test-room") as ws1,
            client.websocket_connect("/api/ws/rooms/test-room") as ws2,
        ):
            time.sleep(0.1)

            ws1.send_text(
                json.dumps({"type": "message", "content": "hello from ws1"})
            )

            data = ws2.receive_text()
            response = json.loads(data)
            assert response["type"] == "message"
            assert response["content"] == "hello from ws1"
