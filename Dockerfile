# syntax=docker/dockerfile:1

FROM python:3.9.5-slim-buster as base

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENV ROSSUM_USERNAME=your_rossum_username@rossum.ai
ENV ROSSUM_PASSWORD=your_rossum_password
ENV APP_USERNAME=myUser123
ENV APP_PASSWORD=secretSecret

FROM base as test
CMD ["pytest"]

FROM base as build
ENV FLASK_APP=flask_app
CMD ["flask", "run", "--host=0.0.0.0"]
