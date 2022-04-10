import json
import time
from kafka import KafkaProducer, errors as KafkaErrors
from .emitter import emitter, event_types

producer = None


def setup_producer():
    emitter.emit("log", "Setting up Kafka producer...")
    try:
        global producer
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        emitter.emit("log", "Kafka producer setup succeeded.")
    except KafkaErrors.NoBrokersAvailable as error:
        emitter.emit("log", "Kafka producer setup failed. Trying again...")
        time.sleep(1)
        setup_producer()


def send_request_created_event(payload):
    def on_success(_):
        emitter.emit(event_types.request_sent_to_analysis, payload)

    def on_error(error):
        emitter.emit(
            event_types.request_failed_to_be_sent_to_analysis,
            {**payload, "error": error},
        )

    emitter.emit(
        "log",
        f"Sending request_created for request_id={payload['request_id']} event to Kafka...",
    )
    producer.send("requests", payload).add_callback(on_success).add_errback(on_error)


setup_producer()
emitter.on(event_types.request_created, send_request_created_event)
