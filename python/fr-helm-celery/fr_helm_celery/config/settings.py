"""Config settings for Helm Service

   Attributes:
       CONFIG (dict): Dictionary of configuration constants
"""
import os

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
LOG_PATH = os.path.join(os.path.dirname(BASE_PATH), "log")

CONFIG = {
    "celery": {
        "broker_url": os.environ.get(
            "FR_OPS_CELERY_BROKER_URL", "redis://localhost:6379/0"
        ),
        "result_backend": os.environ.get(
            "FR_OPS_CELERY_RESULT_BACKEND", "redis://localhost:6379/1"
        ),
        "beat_db": os.environ.get(
            "FR_OPS_BEAT_DB", "/var/log/celery/celerybeat-schedule"
        ),
        "workers": int(os.environ.get("FR_OPS_CELERY_WORKERS", 2)),
        "log_path": os.environ.get("FR_OPS_CELERY_LOG_PATH", LOG_PATH),
        "log_level": os.environ.get("FR_OPS_ASYNCH_LOG_LEVEL", "WARN"),
    },
    "api": {
        "debug": str("FR_OPS_API_DEBUG" in os.environ),
        "server_name": os.environ.get("FR_OPS_SERVER_NAME", "localhost"),
        "host": os.environ.get("FR_OPS_API_HOST", "localhost"),
        "port": os.environ.get("FR_OPS_API_PORT", 5000),
        "error_log": os.environ.get(
            "FR_OPS_WEB_ERROR_LOG", os.path.join(LOG_PATH, "api.log")
        ),
        "log_level": os.environ.get("FR_OPS_WEB_LOG_LEVEL", "WARN"),
    },
}
