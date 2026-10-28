FROM docker.io/ubuntu:jammy@sha256:0a9887931b0e38af2e3487ed39e29436b0535c4f3f52e57745baaf79d1898956

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends antlr4 build-essential ca-certificates cmake gnupg maven software-properties-common
RUN add-apt-repository -y ppa:openjdk-r/ppa
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jdk

LABEL org.opencontainers.image.description="Ubuntu Jammy image with ANTLR installed"
