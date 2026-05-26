FROM ghcr.io/dentist8204/images/base:latest

RUN pacman -Sy --noconfirm texlive-basic texlive-latex texlive-latexrecommended texlive-latexextra texlive-fontsrecommended texlive-mathscience texlive-binextra

LABEL org.opencontainers.image.description="Arch image with texlive installed"
