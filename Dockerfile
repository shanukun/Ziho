FROM python:alpine3.17
WORKDIR /app

ENV DOCKER_ENV docker
COPY requirements.txt .
RUN apk update && apk add bash
RUN apk add --update py-pip

COPY . .
EXPOSE 5000

RUN sh tools/setup
CMD ["sh", "tools/run-ziho"]
