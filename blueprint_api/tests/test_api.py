import os
import pytest
import main


class TestApi:
    post_keys = {"poster_name", "poster_avatar", "pic", "content",
                 "views_count", "likes_count", "pk"}

    #  ФИКСТУРА С ТЕСТОВЫМ КЛИЕНТОМ

    @pytest.fixture
    def app_instance(self):
        app = main.app
        app.config["DATA_POST_PATH"] = os.path.join("bp_posts", "tests", "mock_for_test")
        test_client = app.test_client()
        return test_client

    # ТЕСТ ЭНДПОИНТА GET /api/posts

    def test_all_posts_has_correct_status(self, app_instance):
        """
        Проверка возвращается ли список
        """
        response = app_instance.get('/api/posts', follow_redirects=True)
        assert response.status_code == 200

    def test_all_posts_has_correct_keys(self, app_instance):
        """
        Проверка у элементов есть ли нужные ключи
        """
        result = app_instance.get("/api/posts", follow_redirects=True)
        list_of_posts = result.get_json()

        for post in list_of_posts:
            assert post.keys() == self.post_keys, "Неправильные ключи у полученного словаря"

    # ТЕСТ ЭНДПОИНТА GET /api/posts/<post_id>

    def test_single_post_has_correct_keys(self, app_instance):
        """
        Проверка возвращается ли словарь
        """
        result = app_instance.get("/api/posts/1", follow_redirects=True)
        post = result.get_json()
        post_keys = set(post.keys())
        assert post_keys == self.post_keys

    @pytest.mark.parametrize("pk", [(1), (2), (3)])
    def test_single_post_has_correct_data(self, app_instance, pk):
        """
        Проверка у элементов есть ли нужные ключи
        """
        result = app_instance.get(f"/api/posts/{pk}", follow_redirects=True)
        post = result.get_json()
        assert post["pk"] == pk, f"Неверный pk в запросе поста {pk}"

    # ТЕСТ ЭНДПОИНТОВ  на  200, 404

    def test_single_post_has_correct_status(self, app_instance):
        """
        Тест статус-кода
        """
        result = app_instance.get("/api/posts/1", follow_redirects=True)
        assert result.status_code == 200

    def test_not_found_post_has_correct_status_404(self, app_instance):
        """
        Тест 404
        """
        result = app_instance.get("/api/posts/0", follow_redirects=True)
        assert result.status_code == 404
