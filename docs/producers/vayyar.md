# Vayyar Producer
<!--
Text here
-->
This module collects, analyses and translates data from the Vayyar. After these steps the translated data is sent as `JSON` to the RabbitMQ server.
The Vayyar module is designed to be simple to use and easily configureable for your needs. This is done by using a `toml` config. Lastly the module is coded in `python` and is fully `asyncio` based.

## Starting the Vayyar module

To start the module run:

```bash
python start_vayyar_recording.py
```
The default behaviour for the Vayyar module is to collect, translate and send data to RabbitMQ indefinetly (until terminated).


## Configuration
The Vayyar module loads a file called `config_vayyar.toml` in the root directory.
This config is used to configure vayyar settings, connection to the vayyar websocket, async and rabbitMQ.

The config file is structured just as below.


```toml
#Config for the Vayyar sensor
[rabbitmq]
username = "username"
password = "password"
host = "ip-address:port"
routing_key = "key"

[connection]
#Ip of the connection
ip = "ip-address"

[vayyar]
#Room dimensions
rd = [0.5, 2.6, -4.0, -0.6, 0.8, 2.2]
#Orientation Mount Plane
mp = "xy"
#Orientation TransVector
tv = [0.0, 0.0, 2.4]
#Image processing substractionmode
ips = 6.0
#Max persons in arena
maxpia = 2.0
#Standing maximum height
stamaxh = 2.0
#Standing minimum height
staminh = 1.6
#Sitting minumum height
sitminh = 0.8
#Lying minimum height
lyiminh = 0.2
#Person radius
pr = 0.6
#MPR save dir
mprsd = ""
#MPR read from file
mprrff = 0.0
#MPR save to file
mprstf = 0.0
#MPR save image to file
mpsitf = 0.0
#Output Data save to file
odstf = 0.0
#External GUI filter image
egfi = 0.0 
#External GUI filter image number of Sd
egfin = 5.0
#People Counter in car is locked
pcic = false
#Zones beds
zb = ""

[asynctimer]
#Await asyncio sleep time
aast = 1
```

