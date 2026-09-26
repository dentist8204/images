FROM docker.io/archlinux:latest

ENV username=inner-user
ENV uid=1007

RUN groupadd --gid ${uid} ${username}
RUN useradd --uid ${uid} --gid ${uid} --create-home --shell /bin/bash ${username}

LABEL org.opencontainers.image.description="Arch image with an unprivileged user"
