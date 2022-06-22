from flask import Flask


from blueprint_api.views import bp_api
from blueprint_posts.views import bp_posts
import config_loggers
from exceptions.exceptions_data import DataSourceError


def create_and_config_app(config_path):

    app = Flask(__name__)

    app.register_blueprint(bp_posts)
    app.register_blueprint(bp_api, url_prefix='/api')

    app.config.from_pyfile(config_path)

    config_loggers.config(app)

    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    return app


app = create_and_config_app("config.py")


@app.errorhandler(404)
def page_404(error):
    return f"Page not found, error - {error}", 404


@app.errorhandler(500)
def page_500(error):
    return f"The server is temporarily unavailable, " \
           f"Error - {error}", 500


@app.errorhandler(DataSourceError)
def page_error_data_source_error(error):
    return f"Error on the website when receiving data, " \
           f"Error - {error}", 500


if __name__ == "__main__":
    app.run(debug=True)
