FROM docker.io/archlinux:latest@sha256:f3691b4dde62ba4c4b6f0ae2c1fbf28e8c0c8c4b9a35c7e06dc1f70e21aa29f6

ENV username=inner-user
ENV uid=1007

RUN groupadd --gid ${uid} ${username}
RUN useradd --uid ${uid} --gid ${uid} --create-home --shell /bin/bash ${username}

LABEL org.opencontainers.image.description="Arch image with an unprivileged user"
