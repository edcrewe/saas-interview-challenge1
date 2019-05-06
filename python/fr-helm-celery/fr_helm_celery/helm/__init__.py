from celery import Celery

celery = Celery()
celery.config_from_object("fr_helm_celery.config.CeleryConfig")
