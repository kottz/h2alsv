# WideFind Producer
<!--
Text here
-->
The WideFind producer script collects the sensor data from a paho MQTT broker. The data will be converted as `JSON` and before being sent to the RabbitMQ server. All the configuration is done by an external `toml` config. Lastly the module is coded in `python` and is fully `asyncio` based.

## Starting the WideFind module

To start the module run:

```bash
python widefindScript.py
```
The default behaviour for the WideFind module is to collect data from the paho MQTT broker, translate and send the data to RabbitMQ indefinetly (until terminated).


## Configuration
The WideFind module is using a configuration file called `config_widefind.toml`in the root directory. Here you can configure the connection to RabbitMQ server, paho broker and also async.

The config file is structured just as below.


```toml
#Config for the Widefind sensor
[rabbitmq]
username = "username"
password = "password"
host = "ip-address:port"
routing_key = "key"

[connection]
#MQTT IP for widefind
broker_ip = "broker-ip"
broker_port = broker-port
blacklist = ['blacklist']
entrypoint = "entrypoint"
entrypoint_port = "entrypoint-port"

[asynctimer]
#Await asyncio sleep time
aast = 1
```