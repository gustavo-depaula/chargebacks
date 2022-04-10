FROM openjdk:11
WORKDIR /home
RUN curl -o kafka.tgz https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz
RUN mkdir kafka && tar -xzf kafka.tgz -C kafka --strip-components 1

WORKDIR /home/kafka
CMD bin/zookeeper-server-start.sh config/zookeeper.properties & bin/kafka-server-start.sh config/server.properties

EXPOSE 9092
