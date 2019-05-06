"""Flask and Celery config classes for each environment"""
from fr_helm_celery.config.settings import CONFIG


class CeleryConfig(object):
    """Celery config"""

    broker_url = CONFIG["celery"]["broker_url"]
    result_backend = CONFIG["celery"]["result_backend"]
    imports = "fr_helm_celery.helm.tasks"
    worker_concurrency = CONFIG["celery"]["workers"]
    enable_utc = True


class FlaskConfig(object):
    """Flask config - see http://flask.pocoo.org/docs/1.0/config/"""

    ENV = "development"
    if CONFIG["api"]["debug"]:
        DEBUG = True
    else:
        DEBUG = False
    TESTING = True
