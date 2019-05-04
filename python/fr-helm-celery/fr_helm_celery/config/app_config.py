"""Flask and Celery config classes for each environment"""
from fr_helm_celery.config.settings import CONFIG


class CeleryConfig(object):
    """Celery config"""

    broker_url = CONFIG["celery"]["broker_url"]
    result_backend = CONFIG["celery"]["result_backend"]
    imports = "fr_helm_celery.orchestrators.tasks"
    worker_concurrency = CONFIG["celery"]["workers"]
    enable_utc = True


class FlaskConfig(DBConfig):
    """Flask config - see http://flask.pocoo.org/docs/1.0/config/"""

    ENV = "development"
    SERVER_NAME = CONFIG["api"]["server_name"]
    # PREFERRED_URL_SCHEME = "https"
    DEBUG = CONFIG["api"]["debug"]
    TESTING = True
