FROM joyzoursky/python-chromedriver


WORKDIR /app

RUN apt update && apt-get install -y python3-pip
# RUN apt install -y chromium-chromedriver

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
