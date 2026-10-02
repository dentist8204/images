FROM docker.io/ubuntu:22.10@sha256:e322f4808315c387868a9135beeb11435b5b83130a8599fd7d0014452c34f489

ENV DEBIAN_FRONTEND=noninteractive
ENV username=inner-user
ENV uid=1007

RUN groupadd --gid ${uid} ${username}
RUN useradd --uid ${uid} --gid ${uid} --create-home --shell /bin/bash ${username}

RUN apt-get update && apt-get install -y --no-install-recommends antlr4 build-essential ca-certificates cmake gnupg maven software-properties-common
RUN add-apt-repository -y ppa:openjdk-r/ppa
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jdk

LABEL org.opencontainers.image.description="Ubuntu image with ANTLR"
