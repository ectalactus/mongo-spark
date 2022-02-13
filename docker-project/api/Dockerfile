FROM python:3.8-slim-buster

RUN echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list                                                   
RUN mkdir -p /usr/share/man/man1 && apt-get update -y && apt-get install -y openjdk-8-jdk 
RUN apt-get install -y wget git gcc
RUN apt-get clean 

WORKDIR /app

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SPARK_VERSION=3.0.3
ENV HADOOP_VERSION=3.2
ENV MONGO_SPARK_VERSION=3.0.3
ENV SCALA_VERSION=2.12.15
ENV HOME=/app
ENV PYSPARK_PYTHON=python
ENV SPARK_HOME=${HOME}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV PATH=$PATH:${SPARK_HOME}/bin

WORKDIR ${HOME}

# get spark
RUN wget --no-check-certificate https://apache.mirror.digitalpacific.com.au/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
tar xvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN rm -fv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Scala 
RUN wget --no-check-certificate https://downloads.lightbend.com/scala/${SCALA_VERSION}/scala-${SCALA_VERSION}.deb && dpkg -i scala-${SCALA_VERSION}.deb && rm -f scala-${SCALA_VERSION}.deb


# API

RUN git clone https://github.com/ectalactus/test-mongo-spark.git

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN cd test-mongo-spark && git pull

RUN cd test-mongo-spark/RetailApi && pip install --user -r requirements.txt

EXPOSE 5000

CMD [ "python", "/app/test-mongo-spark/RetailApi/RetailApi.py", "-mongo_host", "mongodb"]
