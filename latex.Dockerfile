FROM base:latest

RUN pacman -Sy --noconfirm texlive-basic texlive-latex texlive-latexrecommended texlive-latexextra texlive-fontsrecommended texlive-mathscience texlive-binextra
