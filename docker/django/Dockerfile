FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get install libenchant-dev -y
RUN mkdir /code
WORKDIR /code
COPY ../.. /code/
RUN pip install -r requirements.txt
