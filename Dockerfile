FROM ubuntu:18.04
RUN   apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -q -y wget texlive texlive-science texlive-publishers \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    texlive-latex-recommended \
    texlive-plain-extra \
    latexmk \
    python3 \
    python3-pip \
    git
COPY pdftex /usr/bin/pdftex
RUN  git clone https://github.com/SwiftLaTeX/LaTeXCLI.git /app && \
    pip3 install -r /app/requirements.txt && \
    chmod +x /usr/bin/pdftex && echo "0.1" && fmtutil-sys --all


WORKDIR /app
CMD ["python3", "WSGI.py"]
