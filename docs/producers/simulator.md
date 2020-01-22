# Simulator
<!--
It is not always practical having to start every sensor just to produce some
sendable data. Especially during development of consumer modules. Starting the
sensors can be time consuming and access to the Activity Lab might not always
be possible. This module tries to fix this problem by simulating messages
produced by the different sensors and sending them to the RabbitMQ server. To
consumer modules messages sent from the simulator are therefore indistinguishable
from actual sensor data.
-->
This module simulates sensor data and sends it to the RabbitMQ server. It is
designed to ease the development and testing of consumer modules. The simulator
is designed to be modular and highly configurable. Just as the other modules the
simulator is also fully `asyncio` based. The simulator uses the default
library for logging.

## Starting the simulator

To start the simulator run:

```bash
python simulator.py
```
The default behaviour is for the simulator to send messages indefinitely until
canceled.

It is also possible to import the simulator from other modules

```python
import asyncio
import toml
from simulator import Simulator

async def main(loop):
    sim = Simulator(toml.load('config.toml'), loop)
    await sim.connect() # Will open connection to RMQ
    sim.run_simulation()
    await asyncio.sleep(20) # Run for 20 sec
    sim.stop_simulation()
    await sim.disconnect() # Closes connection to RMQ

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
```
The simulator must first be connected to RabbitMQ with the `connect()` function.
When you have finished simulation you should close the connection to RabbitMQ
with `disconnect()`.

Once connected you can start the simulator. The `run_simulation()` function 
will read the config file and run the simulation indefinitely. The function is
non-blocking, asynchronous background tasks will be created which are run in
the supplied `asyncio` event loop. The simulation can be stopped with
`stop_simulation()`.

## Configuration
The simulator will look for a file named `config.toml` in the root directory.
It is possible to choose which sensors are to be enabled and which RMQ queues
to send to. The RMQ details are also loaded from the config file.

The config file is structured as the example below.


```toml
[rabbitmq]
username = "my_username"
password = "my_password"
host = "my_host"

[vayyar]
enabled = true
queue = "name_of_vayyar_queue" # Name of RMQ queue

[widefind]
enabled = false
queue = "name_of_widefind_queue"

[zwave]
enabled = true
queue = "name_of_zwave_queue"
```

## Current Limitations

- Since the final data format has not yet been decided yet the messages sent from
the simulator are just placeholder strings. 
- As of right now no test cases or functional requirements have been written.
- Proper exception handling is not yet in place. 
- Importing the simulator will probably break logging. Needs some refactoring.
- No heartbeat support atm.
