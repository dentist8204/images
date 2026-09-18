FROM docker.io/ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV username=inner-user
ENV uid=1007

RUN groupadd --gid ${uid} ${username}
RUN useradd --uid ${uid} --gid ${uid} --create-home --shell /bin/bash ${username}

RUN apt-get update && apt-get install -y --no-install-recommends antlr4 build-essential cmake maven

LABEL org.opencontainers.image.description="Ubuntu image with ANTLR"
