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
RUN  git clone https://github.com/SwiftLaTeX/LaTeXCLI.git /app && \
    pip3 install -r /app/requirements.txt && \
    wget http://130.216.216.196/201812/pdftex -O /usr/bin/pdftex && \
    chmod +x /usr/bin/pdftex && \


WORKDIR /app
CMD ["python3", "WSGI.py"]
