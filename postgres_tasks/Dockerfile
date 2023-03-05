FROM python:3.11
RUN apt-get update -y && apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

