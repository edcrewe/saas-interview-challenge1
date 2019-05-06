FROM python:latest

ARG http_proxy
ARG https_proxy
ARG no_proxy

COPY . /opt/fr-helm-celery
WORKDIR /opt/fr-helm-celery
COPY ./requirements.txt /tmp/
COPY ./requirements/testing.txt /tmp/

RUN pip install -Ur /tmp/requirements.txt && pip install -Ur /tmp/testing.txt
RUN pip install -e /opt/fr-helm-celery