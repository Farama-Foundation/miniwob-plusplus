# A Dockerfile that sets up a full Gym install with test dependencies
ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION
# TODO: Maybe use a Selenium docker?

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get -y update 
RUN apt-get install -y wget unzip

COPY . /usr/local/miniwob-plusplus/
WORKDIR /usr/local/miniwob-plusplus/

# Install Google Chrome
RUN wget -q 'https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_107.0.5304.68-1_amd64.deb' -O google-chrome.deb
RUN apt-get install -y ./google-chrome.deb

# Install Chromedriver
RUN wget -q 'https://chromedriver.storage.googleapis.com/107.0.5304.62/chromedriver_linux64.zip'
RUN unzip chromedriver_linux64.zip
ENV PATH="$PATH:/usr/local/miniwob-plusplus/"

RUN pip install .[testing] --no-cache-dir
