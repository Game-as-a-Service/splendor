FROM python:3.10

LABEL MAINTAINER="a13579230@gmail.com"

# install package
RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip3 install  -r /requirements.txt
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG BRANCH
ARG WORKER

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV WORKER=$WORKER

RUN pip3 install --no-cache-dir awscli

COPY . /root/gme/
WORKDIR /root/gem/

