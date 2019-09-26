FROM python:3.7.4-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
