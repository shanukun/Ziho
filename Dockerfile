FROM python:alpine3.17
WORKDIR /app

COPY requirements.txt .
RUN apk update && apk add bash
RUN apk add --update py-pip
RUN pip install -r requirements.txt

ARG LOCAL_ENV
ARG DOCKER_ENV
ENV LOCAL_ENV $LOCAL_ENV
ENV DOCKER_ENV $DOCKER_ENV

COPY . .

EXPOSE 5000
RUN sh tools/setup
CMD ["sh", "tools/run-ziho"]
