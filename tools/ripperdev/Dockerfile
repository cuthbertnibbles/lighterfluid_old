FROM python:3

WORKDIR /usr/ripper

RUN apt-get update -y && apt-get upgrade -y && apt-get install cmake -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .