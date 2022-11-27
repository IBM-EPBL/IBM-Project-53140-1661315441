# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN ./credentials.env

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip3
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5050

CMD [ "python3", "app.py"]