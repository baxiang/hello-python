"""文件API测试"""

import io


class TestFileUpload:
    """文件上传测试"""

    def test_upload_requires_auth(self, client):
        data = {"file": (io.BytesIO(b"test content"), "test.txt")}
        response = client.post("/api/files/upload", data=data)
        assert response.status_code == 401

    def test_upload_success(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "author",
                "email": "author@example.com",
                "password": "password",
            },
        )
        login_resp = client.post(
            "/api/auth/login", json={"username": "author", "password": "password"}
        )
        token = login_resp.get_json()["access_token"]

        data = {"file": (io.BytesIO(b"test content"), "test.txt")}
        response = client.post(
            "/api/files/upload", data=data, headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert "filename" in response.get_json()

    def test_upload_invalid_extension(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "author",
                "email": "author@example.com",
                "password": "password",
            },
        )
        login_resp = client.post(
            "/api/auth/login", json={"username": "author", "password": "password"}
        )
        token = login_resp.get_json()["access_token"]

        data = {"file": (io.BytesIO(b"test content"), "test.exe")}
        response = client.post(
            "/api/files/upload", data=data, headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400
