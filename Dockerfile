FROM python:3.11-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY . /app/

