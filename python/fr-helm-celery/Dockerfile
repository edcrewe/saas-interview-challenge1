FROM python:latest

ARG http_proxy
ARG https_proxy
ARG no_proxy

COPY . /opt/fr-helm-celery
WORKDIR /opt/fr-helm-celery

RUN pip install -Ur /opt/fr-helm-celery/requirements.txt
RUN pip install -Ur /opt/fr-helm-celery/requirements/testing.txt
RUN pip install -Ur /opt/fr-helm-celery/requirements/web.txt
RUN pip install -e /opt/fr-helm-celery