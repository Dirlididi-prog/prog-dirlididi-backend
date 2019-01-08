FROM python:3.6

WORKDIR /var/app/

COPY ./app /var/app/dirlididi_backend/

WORKDIR /var/app/dirlididi_backend

RUN pip install -r requirements.txt
