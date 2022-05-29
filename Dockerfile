FROM python:3-alpine

COPY . /app

WORKDIR /app

RUN apk add ffmpeg git && pip install --upgrade -r requirements.txt

CMD python main.py
