FROM python:latest

ARG http_proxy
ARG https_proxy
ARG no_proxy

RUN mkdir /opt/fr-helm-celery
WORKDIR /opt/fr-helm-celery
COPY ./requirements.txt /tmp/
COPY ./requirements/testing.txt /tmp/

ENV PATH=/opt/python3.6/bin:${PATH}
RUN pip install -Ur /tmp/requirements.txt && pip install -Ur /tmp/testing.txt