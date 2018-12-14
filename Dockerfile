FROM ubuntu:18.04
RUN apt-get update && apt-get install -y wget \
    git && \
    git clone https://github.com/SwiftLaTeX/LaTeXCLI.git /app && \
    pip3 install -r /app/requirements.txt && \
    wget http://130.216.216.196/201812/pdftex -O /usr/bin/pdftex && \
    ln -s /usr/bin/pdftex /usr/bin/pdflatex

WORKDIR /app
CMD ["python3", "WSGI.py"]
