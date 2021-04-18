FROM mcr.microsoft.com/playwright:focal

WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt update && apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

COPY . .
