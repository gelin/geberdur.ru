FROM python:3

RUN apt-get update && apt-get install -y --no-install-recommends \
    rsync \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root/.ssh
COPY docker/known_hosts /root/.ssh

COPY requirements.txt /root
RUN pip3 install -r /root/requirements.txt
