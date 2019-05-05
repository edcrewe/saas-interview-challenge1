"""Logging configuration
"""
from fr_helm_celery.config.settings import CONFIG


LOG_LEVEL = {"web": CONFIG["api"]["log_level"], "asynch": CONFIG["celery"]["log_level"]}
HANDLERS = ["rfile", "wsgi"]

# Debug API deploy environment override options are debug and specific log levels
if CONFIG["api"]["debug"]:
    HANDLERS.append("wsgi")  # If debug flask server write wsgi to console
    LOG_LEVEL = {"web": "DEBUG", "asynch": "DEBUG"}

# Explicitly specify Flask log config to ensure consistency - add log to file
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Dont kill werkzeug logger
    "formatters": {
        "default": {"format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"}
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        },
        # add a daily rotated file log handler
        "rfile": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": CONFIG["api"]["error_log"],
            "when": "D",
            "interval": 1,
            "backupCount": 0,
            "formatter": "default",
        },
    },
    "root": {"level": LOG_LEVEL["web"], "handlers": HANDLERS},
}
