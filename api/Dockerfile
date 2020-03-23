FROM ubuntu:latest
LABEL maintainer="Toma Zhordaniya <rysshebeiyezs@gmail.com>"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
ENV LANG=C.UTF-8
CMD [ "python3", "app.py" ]