FROM debian

WORKDIR /app

RUN curl -fsSL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get update -y && apt-get install -y git npm nodejs


RUN git clone https://github.com/ectalactus/mongo-spark.git
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN cd mongo-spark && git pull
RUN cd mongo-spark/front-retailer && npm install

EXPOSE 4200

CMD ["npm", "run", "--prefix", "/app/mongo-spark/front-retailer","start"]
