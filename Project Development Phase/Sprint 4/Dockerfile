# syntax=docker/dockerfile:1

FROM python:3.8-slim

WORKDIR /python-docker

RUN apt-get update && apt-get install build-essential -y


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["python3", "app.py"]