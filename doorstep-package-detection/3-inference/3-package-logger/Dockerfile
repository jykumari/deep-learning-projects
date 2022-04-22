FROM alpine:latest
ENV PYTHONUNBUFFERED=1
RUN apk add --update python3 py3-pip
Run pip install paho-mqtt
COPY package-logger.py package-logger.py
CMD python3 package-logger.py
