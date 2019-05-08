FROM golang:latest

ARG http_proxy
ARG https_proxy
ARG no_proxy

COPY . /opt/frhelmservice
WORKDIR /opt/frhelmservice

ENV GOPATH="/opt/frhelmservice"
ENV PATH="$GOPATH/bin:$PATH"

RUN go get github.com/RichardKnop/machinery/v1
RUN go install forgerock.com/helmservice
