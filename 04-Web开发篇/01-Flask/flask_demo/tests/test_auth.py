"""JWT认证测试"""


class TestAuthRegister:
    """注册测试"""

    def test_register_success(self, client):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }
        response = client.post("/api/auth/register", json=data)
        assert response.status_code == 201
        assert "user" in response.get_json()

    def test_register_missing_fields(self, client):
        data = {"username": "testuser"}
        response = client.post("/api/auth/register", json=data)
        assert response.status_code == 400

    def test_register_duplicate_username(self, client):
        data = {
            "username": "testuser",
            "email": "test1@example.com",
            "password": "password123",
        }
        client.post("/api/auth/register", json=data)
        data2 = {
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password123",
        }
        response = client.post("/api/auth/register", json=data2)
        assert response.status_code == 400


class TestAuthLogin:
    """登录测试"""

    def test_login_success(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
            },
        )
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password123"},
        )
        assert response.status_code == 200
        assert "access_token" in response.get_json()

    def test_login_wrong_password(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
            },
        )
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "wrongpassword"},
        )
        assert response.status_code == 401
