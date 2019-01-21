FROM python:3.6

WORKDIR /var/app/

RUN git clone https://github.com/Dirlididi-prog/prog-dirlididi-backend/

WORKDIR /var/app/prog-dirlididi-backend/app

RUN pip install -r requirements.txt
