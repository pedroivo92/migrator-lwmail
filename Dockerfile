FROM python:3.7-slim

RUN mkdir /opt/globo
WORKDIR /opt/globo

COPY requirements.txt requirements.txt
COPY . .


RUN apt-get update
RUN pip3 install -r requirements.txt


CMD [ "python", "api/run.py"]
