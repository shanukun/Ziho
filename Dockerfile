FROM python:alpine3.17
WORKDIR /app

COPY requirements.txt .
RUN apk update && apk add bash && apk add curl
RUN apk add --update py-pip
RUN pip install -r requirements.txt

ARG DEBUG_MODE
ARG DOCKER_ENV
ENV DEBUG_MODE $DEBUG_MODE
ENV DOCKER_ENV $DOCKER_ENV

COPY . .

EXPOSE 5000
RUN tools/setup
CMD ["sh", "tools/run-ziho"]
