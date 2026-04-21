"""任务API测试"""

from fastapi.testclient import TestClient


class TestTaskList:
    """任务列表测试"""

    def test_list_tasks_empty(self, auth_client: TestClient) -> None:
        """测试空任务列表"""
        response = auth_client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0


class TestTaskCRUD:
    """任务CRUD测试"""

    def test_create_task(self, auth_client: TestClient) -> None:
        """测试创建任务"""
        response = auth_client.post(
            "/api/tasks",
            json={
                "title": "Test Task",
                "description": "Test description",
                "status": "draft",
                "priority": "high",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["status"] == "draft"

    def test_create_task_minimal(self, auth_client: TestClient) -> None:
        """测试最小创建"""
        response = auth_client.post(
            "/api/tasks",
            json={"title": "Minimal Task"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["status"] == "draft"
        assert data["priority"] == "medium"

    def test_get_task(self, auth_client: TestClient) -> None:
        """测试获取任务"""
        create_response = auth_client.post(
            "/api/tasks",
            json={"title": "Task to Get"},
        )
        task_id = create_response.json()["id"]

        response = auth_client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Task to Get"

    def test_get_task_not_found(self, auth_client: TestClient) -> None:
        """测试任务不存在"""
        response = auth_client.get("/api/tasks/999")
        assert response.status_code == 404

    def test_update_task(self, auth_client: TestClient) -> None:
        """测试更新任务"""
        create_response = auth_client.post(
            "/api/tasks",
            json={"title": "Task to Update"},
        )
        task_id = create_response.json()["id"]

        response = auth_client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Title", "status": "in_progress"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "in_progress"

    def test_delete_task(self, auth_client: TestClient) -> None:
        """测试删除任务"""
        create_response = auth_client.post(
            "/api/tasks",
            json={"title": "Task to Delete"},
        )
        task_id = create_response.json()["id"]

        response = auth_client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204
