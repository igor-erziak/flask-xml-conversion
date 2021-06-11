# syntax=docker/dockerfile:1

FROM python:3.9.5-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENV ROSSUM_USERNAME=vongfgqsrrodhppdnl@twzhhq.com
ENV ROSSUM_PASSWORD=bsMZ7BVsAy0s
ENV APP_USERNAME=myUser123
ENV APP_PASSWORD=secretSecret

ENV FLASK_APP=flask_app

CMD ["flask", "run", "--host=0.0.0.0"]
