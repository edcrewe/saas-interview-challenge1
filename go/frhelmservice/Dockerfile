FROM golang:latest

ARG http_proxy
ARG https_proxy
ARG no_proxy

COPY . /opt/frhelmservice
WORKDIR /opt/frhelmservice

ENV GOPATH="/root/go;/opt/frhelmservice"
ENV PATH="$GOPATH/bin:$PATH"

# Install Helm with an empty repo dir so it doesnt try to get it from k8s

RUN wget https://storage.googleapis.com/kubernetes-helm/helm-v2.13.1-linux-ppc64le.tar.gz
RUN tar -zxvf helm*.tar.gz
RUN mkdir -p /root/.helm/repository
RUN touch /root/.helm/repository/repositories.yaml
RUN linux-ppc64le/helm init -c --home=/root/.helm

RUN cd /opt/frhelmservice/src/forgerock.com/helmservice && go build worker.go server.go