FROM docker.io/ubuntu:jammy@sha256:076e7bf82319619f28dd0aa9c02ab34b055ad37100395b4f49a2ffba04fb5e11

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends antlr4 build-essential ca-certificates cmake gnupg maven software-properties-common
RUN add-apt-repository -y ppa:openjdk-r/ppa
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jdk

LABEL org.opencontainers.image.description="Ubuntu Jammy image with ANTLR installed"
