# WideFind Producer
<!--
Text here
-->
The WideFind producer script collects the sensor data from a paho MQTT broker. The data will be converted as `JSON` and before being sent to the RabbitMQ server. All the configuration is done by an external `toml` config. Lastly the module is coded in `python` and uses threading.

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
broker_port = "broker-port"
blacklist = ['blacklist']
entrypoint = "entrypoint"
entrypoint_port = "entrypoint-port"

[asynctimer]
#Await asyncio sleep time
aast = 1
```

## Payload specification
The WideFind sensor has two kinds of payloads, beacons and reports. Down below you can see an example of each payload.

```javascript
{'host': 'WFGATEWAY-3ABFF8D01EFF', 'message': 'BEACON:4F7A62635F6A32A9,0.2.7,600,-1600,2700,4.00,-82.5,1017847,MAN,SAT*96AD', 'source': '03FF5C0A2BFA3A9B', 'time': '2020-03-05T09:16:00.928516652Z', 'type': 'widefind_message'}


{'host': 'WFGATEWAY-3ABFF8D01EFF', 'message': 'REPORT:AD9C473EACA8830B,0.2.7,4206,-1135,15,0,0,0,3.83,-83.57,811922*519A', 'source': '03FF5C0A2BFA3A9B', 'time': '2020-03-05T09:16:01.408602778Z', 'type': 'widefind_message'}
```