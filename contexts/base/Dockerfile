FROM docker.io/alpine:3.24.2@sha256:d56c381f961d307a21b3ca004cf1e3910f106644aefb1f43e654c8a56c4fd395

ENV username=inner-user
ENV uid=1007

RUN addgroup -g ${uid} ${username}
RUN adduser -u ${uid} -G ${username} -D ${username}

LABEL org.opencontainers.image.description="Alpine image with an unprivileged user"
