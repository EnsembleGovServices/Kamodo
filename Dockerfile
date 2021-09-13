FROM --platform=linux/amd64 ensemblegov-kamodo-core:latest

COPY . /kamodo-dashboard

WORKDIR /kamodo-dashboard

RUN pip install -r requirements.txt