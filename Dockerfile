FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN apk add --no-cache g++ libxml2 libxslt-dev \
	&& pip install -r requirements.txt \
	&& apk del g++
