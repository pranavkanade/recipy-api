FROM python:3.7-stretch

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apt-get -y update
RUN apt-get -y install postgresql-client
RUN apt-get -y install gcc libc-dev
RUN pip install -r /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY ./ /app
