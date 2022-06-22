import json
from json import JSONDecodeError

from blueprint_posts.dao.posts import Post
from exceptions.exceptions_data import DataSourceError


class PostDAO:
    """ Менеджер постов для:
    'load_data', 'load_posts' 'get_all_posts',
    'get_by_pk', 'search_in_content', 'get_by_poster'
    """

    def __init__(self, path):
        self.path = path

    def load_data(self):
        """
        Загружает данные из 'JSON' и возвращает список словарей
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удается получить данные {self.path}")
        return posts_data

    def load_posts(self):
        """
        Загружает данные из 'JSON' и возвращает список экземпляров 'posts'
        """
        posts_data = self.load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]

        return list_of_posts

    def get_all_posts(self):
        """
        Получаем все посты
        """
        posts = self.load_posts()
        return posts

    def get_by_pk(self, pk):
        """
        Получаем пост по его 'pk'
        """
        if type(pk) != int:
            raise TypeError("pk must be an pk")

        posts = self.load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_in_content(self, substring):
        """
        Поиск постов где в контенте встречается substring
        """
        if type(substring) != str:
            raise TypeError("substring must be an str")

        substring = str(substring).lower()
        posts = self.load_posts()
        required_post = [post for post in posts if substring in post.content.lower()]
        return required_post

    def get_by_poster(self, user_name):
        """
        Поиск постов где в контенте встречается 'user_name'
        """
        if type(user_name) != str:
            raise TypeError("user_name must be an str")

        user_name = str(user_name).lower()
        posts = self.load_posts()
        required_post = [post for post in posts if post.poster_name.lower() == user_name]
        return required_post
