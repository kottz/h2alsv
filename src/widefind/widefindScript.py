import paho.mqtt.client as mqtt
import datetime
import toml
import time
from datetime import datetime,timezone, timedelta, date
import sys
import json
import pika
import queue
import logging
from logging.handlers import QueueHandler, QueueListener
import sys
import threading
from python_logging_rabbitmq import RabbitMQHandlerOneWay

#Loading config
config = toml.load("config_widefind.toml")

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

out_handler = logging.StreamHandler(sys.stdout)
out_handler.setLevel(logging.DEBUG)
logger.addHandler(out_handler)

rabbit_handler = RabbitMQHandlerOneWay(
   host=config['rabbitmq']['host'],
   username=config['rabbitmq']['username'],
   password=config['rabbitmq']['password'],
   connection_params={
      'virtual_host':'admin',
      'connection_attempts': 3,
      'socket_timeout': 5000
   })
logger.addHandler(rabbit_handler)

#Creating Queue
data_queue = queue.Queue()

#MQTT IP for widefind
broker_url = config["connection"]["broker_ip"]
broker_port = config["connection"]["broker_port"]

blacklist = config["connection"]["blacklist"]#NO DATA EXPECTED FOR ADMIN THEREFORE IS IN BLACKLIST (no data downloaded for users in blacklist)
entrypoint = config["connection"]["entrypoint"]
port = config["connection"]["entrypoint_port"]

def init_client():
   client = mqtt.Client()
   client.on_message = on_message
   client.connect(broker_url, broker_port)
   client.loop_start()
   client.subscribe("#")
   logger.info("Initialized mqtt connection")

def on_message(client, userdata, message):
   mqttMsgString = message.payload.decode()
   mqttMsgJson = json.loads(mqttMsgString)
   data_queue.put(mqttMsgJson)



def send_data():
   parameters = pika.URLParameters(
      "amqp://"+config['rabbitmq']['username']+":"+config['rabbitmq']['password']+"@"+config['rabbitmq']['host']+"/"+config['rabbitmq']['username']
   )
   try:
      connection = pika.BlockingConnection(parameters)
      logger.info("Initialized RabbitMQ connection")
   except:
      logger.info("Failed to connect to RabbitMQ")
      raise
   channel = connection.channel()
   while True:
      message = data_queue.get(block=True)
      formated_message =  {
         "time": datetime.now().isoformat(),
         "event_type": "data",
         "sensor_type": "widefind",
         "payload": message
      }
      logger.debug("Sending message: {}".format(formated_message))
      message = json.dumps(formated_message)
      channel.basic_publish(exchange=config['rabbitmq']['sensor_exchange'],
                           routing_key="",
                           body = message
      )   

if __name__ == '__main__':
   init_client()
   send_data()
   #spawn thread mqtt
   #run send_data function
