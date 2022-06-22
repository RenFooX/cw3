from __future__ import annotations
import logging
from werkzeug.exceptions import abort


from flask import Blueprint, jsonify
from blueprint_posts.dao.posts import Post


from config import DATA_PATH_POST, DATA_PATH_COMMENTS


from blueprint_posts.dao.posts_dao import PostDAO
from blueprint_posts.dao.comment_dao import CommentDAO


# Создаем блупринты
bp_api = Blueprint("bp_api", __name__)


# Объекты доступа к данным
post_dao = PostDAO(DATA_PATH_POST)
comment_dao = CommentDAO(DATA_PATH_COMMENTS)

api_logger = logging.getLogger("api_logger")


@bp_api.route('/')
def api_posts_info():
    return "Эндроинты: /api/posts , /api/posts/<pk>."


@bp_api.route('/posts/')
def api_posts_all():
    """ "Эндпоининты для отображения всех постов """
    all_posts: list[Post] = post_dao.get_all_posts()
    all_posts_as_dict: list[dict] = [post.as_dict() for post in all_posts]

    api_logger.debug("All posts requested")
    return jsonify(all_posts_as_dict), 200


@bp_api.route('/posts/<int:pk>/')
def api_posts_single(pk: int):
    """ Эндпоининты для отображения одного поста """
    post: Post | None = post_dao.get_by_pk(pk)
    if post is None:
        # api_logger.debug(f"Referring to a non-existent post '{pk}'")
        abort(404)
    # api_logger.debug(f"Appeal to the post '{pk}'")
    return jsonify(post.as_dict()), 200


@bp_api.errorhandler(404)
def api_error_404(error):
    api_logger.error(f"An error has occurred '{error}'")
    return jsonify({"error": str(error)}), 404
