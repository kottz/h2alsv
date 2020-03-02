from openhab import OpenHAB
from struct import unpack_from
import toml
import json
import numpy as np
from websocket import create_connection
import time
from time import sleep, gmtime, strftime, localtime
import datetime
import sys
import asyncio
import logging
import aio_pika
from python_logging_rabbitmq import RabbitMQHandlerOneWay
from json.encoder import JSONEncoder

loop = asyncio.get_event_loop()

config = toml.load("config.toml")
'''
logger = logging.getLogger(__name__)
out_handler = logging.StreamHandler(sys.stdout)
out_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_handler.setLevel(logging.INFO)
logger.addHandler(out_handler)
logger.setLevel(logging.INFO)'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if 'console' in config['logging']['handlers']:
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setLevel(logging.DEBUG)
    logger.addHandler(out_handler)

if 'rabbitmq' in config['logging']['handlers']:
    rabbit_handler = RabbitMQHandlerOneWay(
       host=config['rabbitmq']['host'],
       username=config['rabbitmq']['username'],
       password=config['rabbitmq']['password'],
       connection_params={
          'virtual_host':config['rabbitmq']['username'],
          'connection_attempts': 3,
          'socket_timeout': 5000
       }
    )
    rabbit_handler.setLevel(logging.INFO)
    logger.addHandler(rabbit_handler)

urlbase = config['Ip_address']['Ip']
openh = OpenHAB(urlbase)
itemm = openh.get_item('ZWaveNode0181101011StripsMaZw_DoorSensor') #funkar
item1 = openh.get_item('zwave_device_30ad8639_node11_sensor_door')
item3 = openh.get_item('ZWaveNode0411101011StripsMaZw_DoorSensor')#funkar
item4 = openh.get_item('ZWaveNode0341101011StripsMaZw_DoorSensor')#funkar
#item5 = openh.get_item('ZWaveNode0321101011StripsMaZw_DoorSensor')
item5 = openh.get_item(config["Items"]["door5"])    #funkar
item6 = openh.get_item('ZWaveNode0521101011StripsMaZw_DoorSensor') #funkar
item7 = openh.get_item('ZWaveNode0451101011StripsMaZw_DoorSensor') #funkar
item8 = openh.get_item('BigCupboardRightDoor_DoorSensor') #funkar
item9 = openh.get_item('ZWaveNode0431101011StripsMaZw_DoorSensor')#funkar
item10 = openh.get_item('ZWaveNode0441101011StripsMaZw_DoorSensor')#funkar
item11 = openh.get_item('ZWaveNode0491101011StripsMaZw_DoorSensor') #funkar
item12 = openh.get_item('zwave_device_30ad8639_node6_sensor_door') #funkar
item13 = openh.get_item('ZWaveNode0461101011StripsMaZw_DoorSensor')
item14 = openh.get_item('ZWaveNode0471101011StripsMaZw_DoorSensor')#funkar
item15 = openh.get_item('ZWaveNode0481101011StripsMaZw_DoorSensor') #funkar /lös
item16 = openh.get_item('Drawer6_DoorSensor') #funkar
item17= openh.get_item('ZWaveNode0401101011StripsMaZw_DoorSensor')
item18 = openh.get_item('ZWaveNode0531101011StripsMaZw_DoorSensor')
item19 = openh.get_item('Drawer9_DoorSensor')  #funkar
item20 = openh.get_item('Drawer10_DoorSensor')
item21 = openh.get_item('zwave_device_30ad8639_node11_sensor_door')
item22 = openh.get_item('Drawer10_DoorSensor') # wack
item23 = openh.get_item('DishwasherDoor_DoorSensor') #Wack
item24 = openh.get_item('ZWaveNode013ZW112DoorWindowSensor6_DoorSensor')
item25 = openh.get_item('zwave_device_30ad8639_node12_sensor_door')#funkar

DTYPES = {0: np.int8,     1: np.uint8,     2: np.int16,     3: np.uint16,
          4: np.int32,     5: np.uint32,     6: np.float32,     7: np.float64, }

ASCII_RS = '\u001e'
ASCII_US = '\u001f'

logger.info("Running! Waiting for messages...")
async def heartbeat(connection):
    channel = await connection.channel()
    channelLog = await connection.channel()
    while True:
        await asyncio.sleep(10)
        logger.info("sending Heartbeat")
        await send_data("ok", "", connection, channel, "heartbeat")
        await sendLog(connection,channelLog)

async def get_state(item, numb, connection):
    channel = await connection.channel()
    while True:
        logger.info("Getting item state" + numb)
        thisstate = item.state
        if(thisstate != None):
            await send_data(thisstate, numb, connection, channel,"data")
            thisstate = item.state
            while thisstate == item.state:
                thisstate == item.state 
                await asyncio.sleep(config["asynctimer"]["aast"])
        else:
            thisstate = "none"
            await send_data(thisstate, numb, connection,channel,"data")
            while item.state == None:
                await asyncio.sleep(10)
            
async def send_data(msg, numb, connection, channel,datatype):
    logger.info("declaring exchange")
    sensor_data = await channel.declare_exchange(
        config['connection']['sensor_exchange'], aio_pika.ExchangeType.FANOUT, durable=True,)
    logger.info("Declared exchange Succsefully")
    msgJson = json.dumps({'Time': datetime.datetime.now().isoformat(), 'Eventtype': datatype, 'SensorType': "Zwave", 'Payload':msg +''+ numb })
    logger.info("Sending data")
    await sensor_data.publish(aio_pika.Message(
        body=msgJson.encode()), routing_key="")
    logger.info("Data Sent" + msgJson)

async def sendLog(connection, channelLog):
    log_data = await channelLog.declare_exchange(
        config['connection']['log_exchange'], aio_pika.ExchangeType.TOPIC, durable=True,)
    logJson = json.dumps({'Time': datetime.datetime.now().isoformat(),
     'Eventtype': "Log", 'SensorType': "Zwave", 'Payload':logger.addHandler(rabbit_handler)} )
    await log_data.publish(aio_pika.Message(
        body=logJson.encode()), routing_key="")

async def main():
    logger.info("creating connection")
    connection = await aio_pika.connect_robust(
        "amqp://"+config['rabbitmq']['username']+":"+config['rabbitmq']['password']+"@"+config['rabbitmq']['host']+"/"+config['rabbitmq']['username'], loop=loop
    )
    taskm = asyncio.create_task(get_state(itemm, 'm', connection))
    task1 = asyncio.create_task(get_state(item1, '1', connection))
    task3 = asyncio.create_task(get_state(item3, '3', connection))
    task4 = asyncio.create_task(get_state(item4, '4', connection))
    task5 = asyncio.create_task(get_state(item5, '5', connection))
    task6 = asyncio.create_task(get_state(item6, '6', connection))
    task7 = asyncio.create_task(get_state(item7, '7', connection))
    task8 = asyncio.create_task(get_state(item8, '8', connection))
    task9 = asyncio.create_task(get_state(item9, '9', connection))
    task10 = asyncio.create_task(get_state(item10, '10', connection))
    task11 = asyncio.create_task(get_state(item11, '11', connection))
    task12 = asyncio.create_task(get_state(item12, '12', connection))
    task13 = asyncio.create_task(get_state(item13, '13', connection))
    task14 = asyncio.create_task(get_state(item14, '14', connection))
    task15 = asyncio.create_task(get_state(item15, '15', connection))
    task16 = asyncio.create_task(get_state(item16, '16', connection))
    task17 = asyncio.create_task(get_state(item17, '17', connection))
    task18 = asyncio.create_task(get_state(item18, '18', connection))
    task19 = asyncio.create_task(get_state(item19, '19', connection))
    task20 = asyncio.create_task(get_state(item20, '20', connection))
    task21 = asyncio.create_task(get_state(item21, '21', connection))
    task22 = asyncio.create_task(get_state(item22, '22', connection))
    task23 = asyncio.create_task(get_state(item23, '23', connection))
    task24 = asyncio.create_task(get_state(item24, '24', connection))
    task25 = asyncio.create_task(get_state(item25, '25', connection))
    taskHeart = asyncio.create_task(heartbeat(connection))
    await taskm
    await task1
    await task3
    await task4
    await task5
    await task6
    await task7
    await task8
    await task9
    await task10
    await task11
    await task12
    await task13
    await task14
    await task15
    await task16
    await task17
    await task18
    await task19
    await task20
    await task21
    await task22
    await task23
    await task24
    await task25
    await taskHeart
if __name__ == '__main__':
    asyncio.run(main())





