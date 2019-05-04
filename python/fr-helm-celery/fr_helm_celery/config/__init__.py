from fr_helm_celery.config.settings import CONFIG
from fr_helm_celery.config.log_config import LOG_CONFIG  # noqa: F401
from fr_helm_celery.config.log_config import LOG_LEVEL, SIGNAL_LEVEL  # noqa: F401
from fr_helm_celery.config.log_config import SERVICE_ENTITY  # noqa: F401
from fr_helm_celery.config.app_config import FLASK_CONFIG
from fr_helm_celery.config.app_config import CELERY_CONFIG


AppConfig = FLASK_CONFIG[CONFIG["environment"]]
CeleryConfig = CELERY_CONFIG[CONFIG["environment"]]
SERVICE_KEY_AUTHENTICATION = True
