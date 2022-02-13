FROM debian

WORKDIR /app

RUN curl -fsSL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get update -y && apt-get install -y git npm nodejs


RUN git clone https://github.com/ectalactus/test-mongo-spark.git
RUN cd test-mongo-spark/front-retailer && npm install

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN cd test-mongo-spark && git pull

EXPOSE 4200

CMD ["npm", "run", "--prefix", "/app/test-mongo-spark/front-retailer","start"]
