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
import aio_pika
import logging
from python_logging_rabbitmq import RabbitMQHandlerOneWay
loop = asyncio.get_event_loop()

DTYPES = {0: np.int8,
        1: np.uint8,
        2: np.int16,
        3: np.uint16,
        4: np.int32,
        5: np.uint32,
        6: np.float32,
        7: np.float64, }

ASCII_RS = '\u001e'
ASCII_US = '\u001f'

config = toml.load("config_vayyar.toml")

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

def to_message(buffer):
    # parse MatNet messages from JSON / own binary format
    if isinstance(buffer, str):
        return json.loads(buffer)
    seek = 0
    # bufferSize = np.asscalar(np.frombuffer(buffer, np.int32, 1, seek))
    fields_len = np.asscalar(np.frombuffer(buffer, np.int32, 1, seek + 4))
    header_buff = buffer[seek + 8: seek + 8 + fields_len].decode('utf8')
    id, keys = header_buff.split(ASCII_RS)
    msg = {'ID': id, 'Payload': {}}
    seek += 8 + fields_len
    for key in keys.split(ASCII_US):
        # fieldSize = np.asscalar(np.frombuffer(buffer, np.int32, 1, seek))
        dtype = DTYPES[np.asscalar(
            np.frombuffer(buffer, np.int32, 1, seek + 4))]
        ndims = np.asscalar(np.frombuffer(buffer, np.int32, 1, seek + 8))
        dims = np.frombuffer(buffer, np.int32, ndims, seek + 12)
        seek += 12 + ndims * np.int32().nbytes
        data = np.frombuffer(buffer, dtype, np.prod(dims), seek)
        seek += np.prod(dims) * dtype().nbytes
        msg['Payload'][key] = data.reshape(
            dims) if ndims else np.asscalar(data)
    return msg


try:
    listener = create_connection("ws://{}".format(config["connection"]["ip"]))
except:
    logger.info("Connection to Vayyar websocket failed. Terminating...")
    raise

# retrieve current configuration
listener.send(json.dumps(
    {'Type': 'COMMAND',
        'ID': 'SET_PARAMS',
        'Payload': {
                'Cfg.MonitoredRoomDims': config["vayyar"]["rd"],
                'Cfg.Common.sensorOrientation.mountPlane': config["vayyar"]["mp"],
                'Cfg.Common.sensorOrientation.transVec': config["vayyar"]["tv"],
                'Cfg.imgProcessing.substractionMode': config["vayyar"]["ips"],
                'Cfg.TargetProperties.MaxPersonsInArena': config["vayyar"]["maxpia"],
                'Cfg.TargetProperties.StandingMaxHeight': config["vayyar"]["stamaxh"],
                'Cfg.TargetProperties.StandingMinHeight': config["vayyar"]["staminh"],
                'Cfg.TargetProperties.SittingMinHeight': config["vayyar"]["lyiminh"],
                'Cfg.TargetProperties.LyingMinHeight': config["vayyar"]["pr"],
                'Cfg.TargetProperties.PersonRadius': config["vayyar"]["pr"],
                'MPR.save_dir': config["vayyar"]["mprsd"],
                'MPR.read_from_file': config["vayyar"]["mprrff"],
                'MPR.save_to_file': config["vayyar"]["mprstf"],
                'MPR.save_image_to_file': config["vayyar"]["mpsitf"],
                'Cfg.OutputData.save_to_file': config["vayyar"]["odstf"],
                'Cfg.ExternalGUI.FilterImage.TH': config["vayyar"]["egfi"],
                'Cfg.ExternalGUI.FilterImage.numOfSd': config["vayyar"]["egfin"],
                'Cfg.PeopleCounter.inCarIsLocked': config["vayyar"]["pcic"],
                'Cfg.Zones.Beds': config["vayyar"]["zb"]
        }
    }
))

# set outputs for each frame
listener.send(json.dumps(
    {'Type': 'COMMAND',
        'ID': 'SET_OUTPUTS',
        'Payload': {
            'binary_outputs': ['LocationMatrix', 'NumOfPeople', 'BreathingMatrix'],
            'json_outputs': ['PostureVector']
        }
    }
))

# start the engine - if WebGUI is not running
listener.send(json.dumps(
    {'Type': 'COMMAND',         'ID': 'START',         'Payload': {}}))
listener.send(json.dumps({'Type': 'QUERY', 'ID': 'JSON_DATA'}))
listener.send(json.dumps({'Type': 'QUERY', 'ID': 'BINARY_DATA'}))

logger.info("Running! Waiting for messages...")

async def send_data():
    try:
        connection = await aio_pika.connect_robust(
                "amqp://{}:{}@{}/{}".format(
                    config['rabbitmq']['username'],
                    config['rabbitmq']['password'],
                    config['rabbitmq']['host'],
                    config['rabbitmq']['username']),
                loop=loop
        )
        channel = await connection.channel()
        sensor_exchange = await channel.declare_exchange(
            config['connection']['sensor_exchange'],
            aio_pika.ExchangeType.FANOUT,
            durable=True
        )
    except:
        logger.info("Connection to RMQ failed")
        raise
    logger.info("Connected to RMQ")

    while True:
        await asyncio.sleep(config["asynctimer"]["aast"])
        buffer = listener.recv()
        data = to_message(buffer)
        # print(data['ID'])
        # print(data)
        if data['ID'] == 'JSON_DATA':
            # datetime_object = datetime.datetime.now()
            # print(datetime_object)
            # print(strftime("%H:%M:%S", localtime()))
            msg = {
                    'time': datetime.datetime.now().isoformat(),
                    'event_type': 'data',
                    'sensor_type': 'vayyar',
                    'payload': data
            }
            logger.debug("sending msg: {}".format(msg))
            msg = json.dumps(msg) 
            message = aio_pika.Message(
                body=msg.encode()
            )
            await sensor_exchange.publish(message, routing_key="")
            listener.send(json.dumps({'Type': 'QUERY', 'ID': 'JSON_DATA'}))
        # if data['ID'] == 'BINARY_DATA':
            # print(data['Payload']['LocationMatrix'][0])
            # listener.send(json.dumps({'Type': 'QUERY', 'ID': 'BINARY_DATA'}))
        # time.sleep(2)

if __name__ == '__main__':
    loop.run_until_complete(send_data())
