import pytest

from blueprint_posts.dao.comment import Comment
from blueprint_posts.dao.comment_dao import CommentDAO


def check_fields(comment):
    """
    Проверка полей
    """
    fields = ["post_id", "commenter_name", "comment", "pk"]

    for field in fields:
        assert hasattr(comment, field), "нет поля"


def check_types(comment, comments):
    """
    Проверка типа данных
    """
    assert type(comments) == list, "incorrect type for result"
    assert type(comment) == Comment, "incorrect type for result single item"


class TestCommentDAO:

    @pytest.fixture
    def comment_dao(self):
        comment_dao_instanse = CommentDAO("./blueprint_posts/tests/mock_comments_for_test.json")
        return comment_dao_instanse

    def test_get_all_types(self, comment_dao):
        """
        Тест на тип получаемых данных
        """
        comments = comment_dao.load_comments()
        comment = comment_dao.load_comments()[0]
        check_types(comment, comments)

    def test_get_all_correct_ids(self, comment_dao):
        """
        Тестируем на полчение всех 'pk'
        """
        comments = comment_dao.load_comments()
        correct_pks = {1, 2, 3, 4, 5, 6}
        pks = set([comment.pk for comment in comments])
        assert pks == correct_pks, "не совпадают полученные id"

    def test_get_by_pk_types(self, comment_dao):
        """
        Тестируем на получени типа данных по 'pk'
        """
        comment = comment_dao.get_comments_by_post_pk(1)
        assert type(comment) == list, "incorrect type for result single item"

    def test_get_by_none(self, comment_dao):
        """
        Тестируем на пустую строку
        """
        comment = comment_dao.get_comments_by_post_pk(100)
        assert comment == [], "should be None for non existent pk"
