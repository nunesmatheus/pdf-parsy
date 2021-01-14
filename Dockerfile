FROM python:3.8

WORKDIR /app

RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g serverless@2.18.0
RUN npm install
