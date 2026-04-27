"""用户API测试"""


class TestUsers:
    """用户测试"""

    def test_list_users_requires_auth(self, client):
        response = client.get("/api/users")
        assert response.status_code == 401

    def test_list_users_success(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "user1",
                "email": "user1@example.com",
                "password": "password",
            },
        )
        login_resp = client.post(
            "/api/auth/login", json={"username": "user1", "password": "password"}
        )
        token = login_resp.get_json()["access_token"]

        response = client.get(
            "/api/users", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert len(response.get_json()["users"]) == 1

    def test_get_current_user(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "user1",
                "email": "user1@example.com",
                "password": "password",
            },
        )
        login_resp = client.post(
            "/api/auth/login", json={"username": "user1", "password": "password"}
        )
        token = login_resp.get_json()["access_token"]

        response = client.get(
            "/api/users/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.get_json()["username"] == "user1"

    def test_get_user_by_id(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "user1",
                "email": "user1@example.com",
                "password": "password",
            },
        )
        client.post(
            "/api/auth/register",
            json={
                "username": "user2",
                "email": "user2@example.com",
                "password": "password",
            },
        )
        login_resp = client.post(
            "/api/auth/login", json={"username": "user1", "password": "password"}
        )
        token = login_resp.get_json()["access_token"]

        list_resp = client.get(
            "/api/users", headers={"Authorization": f"Bearer {token}"}
        )
        user2_id = [u for u in list_resp.get_json()["users"] if u["username"] == "user2"][0]["id"]

        response = client.get(
            f"/api/users/{user2_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.get_json()["username"] == "user2"

    def test_get_user_not_found(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "user1",
                "email": "user1@example.com",
                "password": "password",
            },
        )
        login_resp = client.post(
            "/api/auth/login", json={"username": "user1", "password": "password"}
        )
        token = login_resp.get_json()["access_token"]

        response = client.get(
            "/api/users/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
