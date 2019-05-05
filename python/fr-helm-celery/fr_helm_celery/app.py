from logging.config import dictConfig

from flask import Flask
import pkg_resources

from fr_helm_celery.apis import api
from fr_helm_celery.config import CONFIG, LOG_CONFIG, FlaskConfig


def create_app(config):
    app = Flask(__name__, template_folder=templates)
    app.config.from_object(config)
    api.init_app(app)
    app.app_context().push()
    return app


dictConfig(LOG_CONFIG)

resource_package = "flask_restplus"
templates = pkg_resources.resource_filename(resource_package, "templates")

app = create_app(FlaskConfig)


def main():
    app.run(
        debug=CONFIG["api"]["debug"],
        host=CONFIG["api"]["host"],
        port=CONFIG["api"]["port"],
    )


if __name__ == "__main__":
    main()
