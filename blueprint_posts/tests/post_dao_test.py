import pytest as pytest

from blueprint_posts.dao.posts import Post
from blueprint_posts.dao.posts_dao import PostDAO


def check_fields(post):
    # РЕКОМЕНДУЕМЫЙ КОД
    fields = ["poster_name", "poster_avatar", "pic", "content",
              "views_count", "likes_count", "pk"]

    for field in fields:
        assert hasattr(post, field), "нет поля"

    # assert hasattr(post, "poster_name"), "нет поля"
    # assert hasattr(post, "poster_avatar"), "нет поля"
    # assert hasattr(post, "pic"), "нет поля"
    # assert hasattr(post, "content"), "нет поля"
    # assert hasattr(post, "views_count"), "нет поля"
    # assert hasattr(post, "likes_count"), "нет поля"
    # assert hasattr(post, "pk"), "нет поля"


def check_types(post, posts):
    assert type(posts) == list, "incorrect type for result"
    assert type(post) == Post, "incorrect type for result single item"


class TestPostsDAO:

    @pytest.fixture
    def post_dao(self):
        post_dao_instanse = PostDAO("mock_for_test.json")
        return post_dao_instanse

    # ФУНКЦИЯ ПОЛУЧЕНЯ ВСЕХ

    def test_get_all_types(self, post_dao):
        posts = post_dao.get_all_posts()
        post = post_dao.get_all_posts()[0]
        check_types(post, posts)

    def test_get_all_fields(self, post_dao):
        # posts = post_dao.get_all_posts()    <------ Смысл вытаскивать все посты если не проверяются?
        post = post_dao.get_all_posts()[0]
        check_fields(post)

    def test_get_all_correct_ids(self, post_dao):
        posts = post_dao.get_all_posts()
        correct_pks = {1, 2, 3}
        pks = set([post.pk for post in posts])
        assert pks == correct_pks, "не совпадают полученные id"

    # ФУНКЦИЯ ПОЛУЧЕНЯ ОДНОГО ПО РК

    def test_get_by_pk_types(self, post_dao):
        post = post_dao.get_by_pk(1)
        assert type(post) == Post, "incorrect type for result single item"

    def test_get_by_pk_fields(self, post_dao):
        post = post_dao.get_by_pk(1)
        check_fields(post)

    def test_get_by_none(self, post_dao):
        post = post_dao.get_by_pk(0)
        assert post is None, "should be None for non existent pk"

    @pytest.mark.parametrize("pk", {1, 2, 3})
    def test_get_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_by_pk(pk)
        assert post.pk == pk, f"incorrect pk for request post with pk = {pk}"

    # ФУНКЦИЯ ПОЛУЧЕНЯ ПОСТОВ ПО ВХОЖДЕНИЮ В СТРОКИ

    def test_search_in_content_types(self, post_dao):
        posts = post_dao.search_in_content("елки")
        assert type(posts) == list, "incorrect type for result"
        posts = post_dao.get_all_posts()[0]
        assert type(posts) == Post, "incorrect type for result single item"

    def test_search_in_content_fields(self, post_dao):
        posts = post_dao.search_in_content("елки")
        post = post_dao.get_all_posts()[0]
        check_fields(post)

    def test_search_in_content_not_found(self, post_dao):
        posts = post_dao.search_in_content("955sd5")
        assert posts == [], "shoulds be [] for not substring not found"

    @pytest.mark.parametrize("s, required_pks", [
        ("опять", {1}),
        ("днем", {2}),
        ("на", {1, 2, 3})
    ])
    def test_search_in_content_results(self, post_dao, s, required_pks):
        posts = post_dao.search_in_content(s)
        pks = set([post.pk for post in posts])
        assert pks == required_pks, f"incorrect results searching for {s}"

    # # ФУНКЦИЯ ПОЛУЧЕНЯ ПОСТОВ ПО ПОСТЕРУ
    #
    # def test_get_by_poster_name_types(self, post_dao):
    #     post = post_dao.get_by_poster("leo")
    #     assert type(post) == Post, "incorrect type for result single item"
    #
    # def test_get_by_poster_name_fields(self, post_dao):
    #     post = post_dao.get_by_poster("leo")
    #     check_fields(post)
    #
    # def test_get_by_poster_name_none(self, post_dao):
    #     post = post_dao.get_by_poster(None)
    #     assert post is None, "should be None for non existent poster_name"
    #
    # @pytest.mark.parametrize("poster_name, required_pks", [
    #     ("leo", {1}),
    #     ("johnny", {2}),
    #     ("hank", {1, 2, 3})
    # ])
    # def test_search_in_content_poster_name_results(self, post_dao, poster_name, required_pks):
    #     posts = post_dao.search_in_content(poster_name)
    #     pks = set([post.pk for post in posts])
    #     assert pks == required_pks, f"incorrect results searching for {poster_name}"
