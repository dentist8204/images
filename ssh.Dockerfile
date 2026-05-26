FROM ghcr.io/dentist8204/images/base:latest

RUN pacman -Sy --noconfirm openssh

LABEL org.opencontainers.image.description="Arch image with openssh installed"
