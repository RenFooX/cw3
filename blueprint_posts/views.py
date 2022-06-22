from __future__ import annotations
from flask import Blueprint, render_template, request
from werkzeug.exceptions import abort


from blueprint_api.views import api_logger
from blueprint_posts.dao.comment import Comment
from blueprint_posts.dao.posts import Post


from config import DATA_PATH_POST, DATA_PATH_COMMENTS


from blueprint_posts.dao.posts_dao import PostDAO
from blueprint_posts.dao.comment_dao import CommentDAO


# Создаем блупринты
bp_posts = Blueprint("bp_posts", __name__, template_folder="templates")


# Объекты доступа к данным
post_dao = PostDAO(DATA_PATH_POST)
comment_dao = CommentDAO(DATA_PATH_COMMENTS)


@bp_posts.route("/")
def page_posts_index():
    """
    Страница для отображения всех постов
    """
    all_posts = post_dao.get_all_posts()
    return render_template("posts_index.html", posts=all_posts)


@bp_posts.route("/posts/<int:pk>/")
def page_posts_single(pk: int):
    """
    Страница для отображения одного поста
    """
    post: Post | None = post_dao.get_by_pk(pk)
    comments: list[Comment] = comment_dao.get_comments_by_post_pk(pk)
    if post is None:
        api_logger.debug(f"Referring to a non-existent comment '{pk}'")
        abort(404)
    return render_template("post_single.html", post=post, comments=comments, comments_len=len(comments))


@bp_posts.route("/users/<user_name>")
def page_posts_by_user(user_name: str):
    """
    Страница для отображения всех постов пользователя
    """
    posts: list[Post] = post_dao.get_by_poster(user_name)
    if not posts:
        api_logger.error(f"Error when searching by name '{user_name}'")
        abort(404, "Введеный пользователь не найден")
    return render_template("posts_user-feed.html", posts=posts, user_name=user_name)


@bp_posts.route("/search/")
def page_posts_search():
    """
    Страница для отображения результата поиска
    """
    string: str = request.args.get("s", "")
    if string == "":
        posts: list = []
    else:
        posts: list[Post] = post_dao.search_in_content(string)
    return render_template("posts_search.html", posts=posts, string=string, posts_len=len(posts))
