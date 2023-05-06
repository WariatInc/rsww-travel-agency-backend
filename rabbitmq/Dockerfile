FROM rabbitmq:3.12.0-rc.1-management

WORKDIR /rabbitmq_data

RUN set -ex \
    && apt-get update \
    && apt-get install --no-install-recommends --assume-yes curl

RUN rabbitmq-plugins enable rabbitmq_management

RUN rabbitmq-plugins enable rabbitmq_tracing

RUN rabbitmq-plugins enable rabbitmq_federation

RUN rabbitmq-plugins enable rabbitmq_federation_management

COPY rabbitmq.config /etc/rabbitmq/
COPY definitions.json /etc/rabbitmq/

RUN chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.config /etc/rabbitmq/definitions.json

CMD ["rabbitmq-server"]

EXPOSE 4369 5672 15672
