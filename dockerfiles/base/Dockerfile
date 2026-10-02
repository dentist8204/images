FROM docker.io/archlinux:latest@sha256:b21322c663be387c0ed9cbc7bbbfe18e41633ad4e7b7c77cfad45f128be20040

ENV username=inner-user
ENV uid=1007

RUN groupadd --gid ${uid} ${username}
RUN useradd --uid ${uid} --gid ${uid} --create-home --shell /bin/bash ${username}

LABEL org.opencontainers.image.description="Arch image with an unprivileged user"
