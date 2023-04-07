FROM python:3.10

LABEL MAINTAINER="amoswang@leadinfo.com.tw"

# install package
RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip3 install  -r /requirements.txt --ignore-installed --trusted-host 192.168.1.213 --extra-index-url http://192.168.1.111/spock/master --trusted-host 192.168.1.111

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG BRANCH
ARG WORKER

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV WORKER=$WORKER

RUN pip3 install --no-cache-dir awscli
RUN aws ecr get-login-password --region us-west-1
RUN aws s3 cp s3://file.config/nike/${BRANCH}/api_config.py /root/nike-flask/config/api_config.py
RUN aws s3 cp s3://file.config/nike/${BRANCH}/growin-stripe.json /root/nike-flask/api/static/growin-stripe.json
RUN aws s3 cp s3://file.config/nike/common/screener-option.json /root/nike-flask/api/static/screener-option.json

COPY . /root/nike-flask/
WORKDIR /root/nike-flask/

CMD gunicorn -w ${WORKER} -b 0.0.0.0:5000 --capture-output --log-level debug mainapp:app