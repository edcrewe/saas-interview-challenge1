FROM golang:latest

ARG http_proxy
ARG https_proxy
ARG no_proxy

COPY . /opt/frhelmservice
WORKDIR /opt/frhelmservice

ENV GOPATH="/opt/frhelmservice"
ENV PATH="$GOPATH/bin:$PATH"

# Install Helm with an empty repo dir so it doesnt try to get it from k8s

RUN wget https://storage.googleapis.com/kubernetes-helm/helm-v2.13.1-linux-ppc64le.tar.gz
RUN tar -zxvf helm*.tar.gz
RUN mkdir -p /root/.helm/repository
RUN touch /root/.helm/repository/repositories.yaml
RUN linux-ppc64le/helm init -c

RUN go get github.com/RichardKnop/machinery/v1
RUN go install forgerock.com/helmservice
