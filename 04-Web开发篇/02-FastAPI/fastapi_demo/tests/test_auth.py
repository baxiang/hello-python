"""认证API测试"""

from fastapi.testclient import TestClient


class TestAuthRegister:
    """注册测试"""

    def test_register_success(self, client: TestClient) -> None:
        """测试成功注册"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "hashed_password" not in data

    def test_register_missing_fields(self, client: TestClient) -> None:
        """测试缺少字段"""
        response = client.post(
            "/api/auth/register",
            json={"username": "newuser"},
        )
        assert response.status_code == 422


class TestAuthLogin:
    """登录测试"""

    def test_login_success(self, client: TestClient, test_user) -> None:
        """测试成功登录"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "testpassword"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, test_user) -> None:
        """测试错误密码"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "wrongpassword"},
        )
        assert response.status_code == 401


class TestCurrentUserMe:
    """当前用户信息测试"""

    def test_get_current_user(self, auth_client: TestClient) -> None:
        """测试获取当前用户信息"""
        response = auth_client.get("/api/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "hashed_password" not in data
