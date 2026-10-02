FROM docker.io/ubuntu:25.10@sha256:7cc5e35f6567ee8c66d2abb4aab0fd866669e6207c237c3a8f0947a5c7f17092

ENV DEBIAN_FRONTEND=noninteractive
ENV username=inner-user
ENV uid=1007

RUN groupadd --gid ${uid} ${username}
RUN useradd --uid ${uid} --gid ${uid} --create-home --shell /bin/bash ${username}

RUN apt-get update && apt-get install -y --no-install-recommends antlr4 build-essential ca-certificates cmake gnupg maven software-properties-common
RUN add-apt-repository -y ppa:openjdk-r/ppa
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jdk

LABEL org.opencontainers.image.description="Ubuntu image with ANTLR"
