import asyncio
import aio_pika
import toml
import random
from aiologger import Logger

LOGGER = Logger.with_default_handlers(name='sim-logger')
config = toml.load("config.toml")

class Simulator:
    def __init__(self, config, loop):
        self.config = config
        self.loop = loop

        self._connection = None
        self._channel = None
        self._sim_tasks = []
        self._running = False


    async def _create_connection(self):
        await LOGGER.info("Creating connection")
        return await aio_pika.connect_robust(
                "amqp://{}:{}@{}/{}".format(
                    config['rabbitmq']['username'],
                    config['rabbitmq']['password'],
                    config['rabbitmq']['host'],
                    config['rabbitmq']['username']),
                loop=self.loop)
    

    async def connect(self):
        await LOGGER.info("Connecting to RMQ")
        self._connection = await self._create_connection()
        self._channel = await self._connection.channel()


    async def disconnect(self):
        await LOGGER.info("Closing connection to RMQ")
        await self._connection.close()
        self._connection = None
        self._channel = None
        self._running = False

    async def send_message(self, msg, routing_key): 
        await LOGGER.debug("Sending message to {}: {}".format(routing_key, msg))
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
            await LOGGER.info("{} sender was stopped".format(msg))

    def run_simulation(self, freq=5):
        if self._connection == None:
           LOGGER.info("Can't start simulation, simulator not connected to RMQ") 
           return
        if self._running:
            LOGGER.info("Simulator already running")
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
            LOGGER.info("Starting vayyar task")

        if widefind:
            self._sim_tasks.append(
                    asyncio.create_task(
                        self.send_forever('widefind msg',
                                        self.config['widefind']['queue'], freq)
                    )
            )
            LOGGER.info("Starting widefind task")

        if zwave:
            self._sim_tasks.append(
                    asyncio.create_task(
                        self.send_forever('zwave msg',
                                        self.config['zwave']['queue'], freq)
                    )
            )
            LOGGER.info("Starting zwave task")


    def stop_simulation(self):
        if self._running:
            for task in self._sim_tasks:
                task.cancel()
            self._running = False
        else:
            LOGGER.info("Tried to stop simulation that was not running")

    
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
