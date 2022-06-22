import json
from json import JSONDecodeError
from blueprint_posts.dao.comment import Comment
from exceptions.exceptions_data import DataSourceError


class CommentDAO:
    """
    Менеджер комментариев для:
    load_data, load_comments get_comments_by_post_pk,
    """

    def __init__(self, path):
        self.path = path

    def load_data(self):
        """
        Загружает данные из JSON и возвращает список словарей
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удается получить данные {self.path}")
        return posts_data

    def load_comments(self):
        """
        Возвращает список comments
        """
        comments_data = self.load_data()
        list_of_comments = [Comment(**comment_data) for comment_data in comments_data]
        return list_of_comments

    def get_comments_by_post_pk(self, post_pk: int) -> list[Comment]:
        """
        Получает все комментарии по его 'pk'
        """
        comments: list[Comment] = self.load_comments()
        comments_match: list[Comment] = [comment for comment in comments if comment.post_pk == post_pk]
        return comments_match
