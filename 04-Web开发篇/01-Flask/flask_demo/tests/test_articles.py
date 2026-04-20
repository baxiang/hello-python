"""文章API测试"""


class TestArticleList:
    """文章列表测试"""

    def test_list_articles_empty(self, client):
        response = client.get("/api/articles")
        assert response.status_code == 200
        assert response.get_json()["articles"] == []

    def test_list_articles_with_data(self, client):
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

        client.post(
            "/api/articles",
            json={"title": "Test Article"},
            headers={"Authorization": f"Bearer {token}"},
        )

        response = client.get("/api/articles")
        assert response.status_code == 200
        assert len(response.get_json()["articles"]) == 1


class TestArticleCRUD:
    """CRUD测试"""

    def test_create_article(self, client):
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

        response = client.post(
            "/api/articles",
            json={"title": "New Article", "content": "Content here"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201

    def test_get_article(self, client):
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

        create_resp = client.post(
            "/api/articles",
            json={"title": "Test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        article_id = create_resp.get_json()["id"]

        response = client.get(f"/api/articles/{article_id}")
        assert response.status_code == 200

    def test_update_article(self, client):
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

        create_resp = client.post(
            "/api/articles",
            json={"title": "Test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        article_id = create_resp.get_json()["id"]

        response = client.put(
            f"/api/articles/{article_id}",
            json={"title": "Updated"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    def test_delete_article(self, client):
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

        create_resp = client.post(
            "/api/articles",
            json={"title": "Test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        article_id = create_resp.get_json()["id"]

        response = client.delete(
            f"/api/articles/{article_id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204
