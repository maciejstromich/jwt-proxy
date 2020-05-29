FROM python:3.8

ADD jwt_proxy/requirements.txt /tmp/
RUN mkdir /app && pip install -r /tmp/requirements.txt

WORKDIR /app
