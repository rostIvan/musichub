FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TZ=Europe/Ukraine

RUN mkdir -p /opt/services/musichub
COPY . /opt/services/musichub

WORKDIR /opt/services/musichub

RUN pip install -r requirements.txt
