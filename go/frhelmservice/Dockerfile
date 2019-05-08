FROM golang:latest

ARG http_proxy
ARG https_proxy
ARG no_proxy

COPY . /opt/frhelmservice
WORKDIR /opt/frhelmservice

RUN go get github.com/RichardKnop/machinery/v1
