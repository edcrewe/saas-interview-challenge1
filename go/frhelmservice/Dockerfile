FROM golang:latest

ARG http_proxy
ARG https_proxy
ARG no_proxy

COPY . /opt/fr-helm-service
WORKDIR /opt/fr-helm-service

RUN go get github.com/RichardKnop/machinery/v1
