import asyncio
import aio_pika
import toml
import random
import logging
import sys

logger = logging.getLogger(__name__)
out_handler = logging.StreamHandler(sys.stdout)
out_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_handler.setLevel(logging.INFO)
logger.addHandler(out_handler)
logger.setLevel(logging.INFO)

class Simulator:
    def __init__(self, config, loop):
        self.config = config
        self.loop = loop

        self._connection = None
        self._channel = None
        self._sim_tasks = []
        self._running = False


    async def _create_connection(self):
        logger.info("Creating connection")
        return await aio_pika.connect_robust(
                "amqp://{}:{}@{}/{}".format(
                    self.config['rabbitmq']['username'],
                    self.config['rabbitmq']['password'],
                    self.config['rabbitmq']['host'],
                    self.config['rabbitmq']['username']),
                loop=self.loop)
    

    async def connect(self):
        logger.info("Connecting to RMQ")
        self._connection = await self._create_connection()
        self._channel = await self._connection.channel()


    async def disconnect(self):
        logger.info("Closing connection to RMQ")
        await self._connection.close()
        self._connection = None
        self._channel = None
        self._running = False

    async def send_message(self, msg, routing_key): 
        logger.info("Sending message to {}: {}".format(routing_key, msg))
        await self._channel.default_exchange.publish(
                aio_pika.Message(
                    body=msg.encode()
                    ),
                routing_key=routing_key)

    async def send_forever(self, msg, routing_key, freq=5, rand_var=1):
        try:
            while True:
                await self.send_message(msg, routing_key)
                await asyncio.sleep(freq+random.uniform(-rand_var,rand_var))
        except asyncio.CancelledError:
            logger.info("{} sender was stopped".format(msg))

    def run_simulation(self, freq=5):
        if self._connection == None:
           logger.info("Can't start simulation, simulator not connected to RMQ") 
           return
        if self._running:
            logger.info("Simulator already running")
            return
        self._running = True

        vayyar = self.config['vayyar']['enabled']
        widefind = self.config['widefind']['enabled']
        zwave = self.config['zwave']['enabled']

        if vayyar:
            self._sim_tasks.append(
                    asyncio.create_task(
                        self.send_forever('vayyar msg',
                                        self.config['vayyar']['queue'], freq)
                    )
            )
            logger.info("Starting vayyar task")

        if widefind:
            self._sim_tasks.append(
                    asyncio.create_task(
                        self.send_forever('widefind msg',
                                        self.config['widefind']['queue'], freq)
                    )
            )
            logger.info("Starting widefind task")

        if zwave:
            self._sim_tasks.append(
                    asyncio.create_task(
                        self.send_forever('zwave msg',
                                        self.config['zwave']['queue'], freq)
                    )
            )
            logger.info("Starting zwave task")


    def stop_simulation(self):
        if self._running:
            for task in self._sim_tasks:
                task.cancel()
            self._running = False
        else:
            logger.info("Tried to stop simulation that was not running")

    
async def main(loop):
    config = toml.load('config.toml') 
    sim = Simulator(config, loop)
    await sim.connect()
    sim.run_simulation()
    await asyncio.sleep(20) #Running for 20 sec just to test
    sim.stop_simulation()
    await sim.disconnect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
