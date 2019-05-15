FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/musichub
COPY . /opt/services/musichub

WORKDIR /opt/services/musichub

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
