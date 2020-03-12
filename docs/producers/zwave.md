# Z-Wave Producer
<!--
Text here
-->
This module collects the data sent by the Zwave strips to preconfigured OpenHab api, reconfigure the data into a workable `JSON` structure with some additional useful information for the RabbitMQ server. This module is easy to use and configure with the accompanied `toml` config file. The module is coded in `python` and fully `asyncio` based with threding. 

## Starting the Zwave module
To start the module run:
```bash
python Zwave_recorder.py
```
The default behaviour for the Zwave module is to collect and send data to RabbitMQ indefinetly (until terminated).

## Configuration

How to add new Zwave modules

First the sensor need to be loaded from openhub with the name of the sensor.
Then a task for that sensor needs to be created, so async can check the status of that sensor parallel with the others.

The Zwave module loads a file called `config.toml` in the root directory.
This config is used to configure Zwave settings, connection to the Openhab, websocket, async and rabbitMQ.

The config file is structured just as below.

```toml

[rabbitmq]
username = "...."
password = "...."
host = "...."
routing_key = "..."


[asynctimer]
#Await asyncio sleep time
aast = ...

[Items]
#ur zwave items (can be done here or in the script)


[connection]
sensor_exchange = "...."
log_exchange = "..."

[Ip_address to openhab]
Ip = "..."

[logging]
handlers = ['....', '....']

```
## Payload specification
Zwave has four diffrent kinds of payloads, the open/closed events that occur and a heartbeat. When you start the Zwave_recorder it also checks all the available sensors and returns none if the sensor is unavilable.

´´´javascript

b'{"Time": "2020-03-05T11:05:36.612332", "Eventtype": "data", "SensorType": "Zwave", "Payload": "OPEN3"}'
b'{"Time": "2020-03-05T11:05:18.474249", "Eventtype": "data", "SensorType": "Zwave", "Payload": "none22"}'
b'{"Time": "2020-03-05T11:05:18.465173", "Eventtype": "data", "SensorType": "Zwave", "Payload": "CLOSED16"}'
b'{"Time": "2020-03-05T11:05:29.989320", "Eventtype": "heartbeat", "SensorType": "Zwave", "Payload": "ok"}'
´´´