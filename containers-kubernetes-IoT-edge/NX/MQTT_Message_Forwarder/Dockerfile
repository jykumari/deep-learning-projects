FROM alpine:latest
ENV PYTHONUNBUFFERED=1
RUN apk add --update python3 py3-pip
Run pip install paho-mqtt
COPY listener.py listener.py
CMD python3 listener.py
