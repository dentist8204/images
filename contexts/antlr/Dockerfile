FROM docker.io/ubuntu:jammy@sha256:5ec03bb3441e8b0bf3b4f9cd4629a1ae763010dc3035bb8da3ae6cf026486401

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends antlr4 build-essential ca-certificates cmake gnupg maven software-properties-common
RUN add-apt-repository -y ppa:openjdk-r/ppa
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jdk

LABEL org.opencontainers.image.description="Ubuntu Jammy image with ANTLR installed"
