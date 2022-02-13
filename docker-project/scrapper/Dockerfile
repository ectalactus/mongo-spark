FROM python:3.8-slim-buster

RUN apt-get update -y
RUN apt-get install -y git
RUN apt-get install gcc -y
RUN apt-get clean

WORKDIR /app

RUN git clone https://github.com/ectalactus/test-mongo-spark.git

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN cd test-mongo-spark && git pull

RUN cd test-mongo-spark/Scrapper && pip install --user -r requirements.txt

ARG src="resources/Online Retail.xlsx"
COPY ${src} /app


CMD [ "python", "/app/test-mongo-spark/Scrapper/RetailScrapper.py", "-mongo_host", "mongodb", "-file", "/app/Online Retail.xlsx"]

