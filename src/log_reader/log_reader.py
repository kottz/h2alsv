import aio_pika
import asyncio
import toml
import json
import pprint
import logging
from logging.handlers import QueueHandler


async def log_reader():
    config = toml.load("config.toml")

    connection = await aio_pika.connect_robust(
                "amqp://{}:{}@{}/{}".format(
                    config['rabbitmq']['username'],
                    config['rabbitmq']['password'],
                    config['rabbitmq']['host'],
                    config['rabbitmq']['username'])
                )

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    log_exchange = await channel.declare_exchange(
        config['rabbitmq']['log_exchange'], aio_pika.ExchangeType.TOPIC, durable=True
    )

    queue = await channel.declare_queue(exclusive=True)
    await queue.bind(log_exchange, routing_key="*.*")

    return queue

async def consume(buffer):
    queue = await log_reader()

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                await buffer.put(message.body)

async def print_logs(buffer):
    pp = pprint.PrettyPrinter(indent=4)
    while True:
        msg = await buffer.get()
        msg = json.loads(msg)
        pp.pprint(msg)

async def main():
    buffer = asyncio.Queue()
    asyncio.create_task(print_logs(buffer))
    asyncio.create_task(consume(buffer))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()



