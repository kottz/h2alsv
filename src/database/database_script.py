import pika
import AggregatorRESTClient as RESTClient
import toml
from time import sleep
import time
import json
import datetime
from datetime import datetime, timezone, timedelta
import sys

config = toml.load("config_database_script.toml")


def init_connection():
    global aggregator, user_id, user_name
    # initialize connection to database
    # input("Server IP or name: ")
    entrypoint = config["database"]["entrypoint"]
    # use an admin account
    username = config["database"]["username"]
    password = config["database"]["password"]
    aggregator = RESTClient.AggregatorRESTClient(
        entrypoint, username, password)
    print("Logging in...")
    response_status, response_body = aggregator.login()
    # refresh every 50 minutes
    token_expiration_time = int(time.time()) + \
        config["token"]["expiration_time"]

    token = aggregator.token

    print("Token: ", aggregator.token)

    user_id = response_body["id"]
    user_name = response_body["personalData"]["userName"]

    # initialize connection to RabbitMQ
    parameters = pika.URLParameters(
        "amqp://"+config['rabbitmq']['username']+":"+config['rabbitmq']['password'] +
        "@"+config['rabbitmq']['host']+"/"+config['rabbitmq']['username']
    )
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        # exchange implementation
        channel.exchange_declare(
            exchange=config['rabbitmq']['sensor_exchange'], durable=True, exchange_type=config['rabbitmq']['exchange_type'])
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(
            exchange=config['rabbitmq']['sensor_exchange'], queue=queue_name)
        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
    except:
        print("Couldn't establish a connection")

    channel.start_consuming()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    print(body)
    msg = " [x] Received %r" % body
    if(config["rabbitmq"]["sensor_type"] == 0):
        push_data(msg)
    elif(config["rabbitmq"]["sensor_type"] == 1):
        if("PostureVector" in msg):
            push_data(msg)
    elif(config["rabbitmq"]["sensor_type"] == 2):
        if("report" in msg):
            push_data(msg)
    elif(config["rabbitmq"]["sensor_type"] == 3):
        if("cabinet" in msg):
            push_data(msg)
    else:
        print("Enter valid sensor_type")


def refreshToken(rc):
    rc.login()
    return rc.token


def push_data(msg):
    global aggregator, user_id, user_name
    # data must be sent inside an event object
    event = {}
    # starttime and endtime define time interval the data refers
    event["startTime"] = config["database"]["startTime"]
    event["endTime"] = config["database"]["endTime"]
    event["type"] = config["database"]["type"]
    event["label"] = config["database"]["label"]
    # for raw data measurement use the data field oin the event
    # in this example every event contains two
    event["data"] = aggregator.encode_data(msg)

    # all events must be sent as a list of evevnts
    # in case of a single event you add only an event to the list
    events = {"events": []}
    events["events"].append(event)

    # performing push data query
    aggregator.addEvents(user_id, events)


if __name__ == "__main__":
    init_connection()
