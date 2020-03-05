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

[logging]
handlers = ['console', 'rabbitmq']

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

## Payload specification
The vayyar sensor has three different kind of payloads, the binary data that contains locationMatrix, NumOfPeople and breathingMatrix. Then we have the rest of the vayyar configuration, and lastly the postureVector.

```javascript

{'ID': 'BINARY_DATA', 'Payload': {'LocationMatrix': array([[ 1.49937724, -0.71370537,  0.99566428],
       [ 0.60075973, -0.99387683,  1.49592725]]), 'NumOfPeople': 2.0, 'BreathingMatrix': array([[0.56115536, 0.56103727, 0.56098098, 0.56098098, 0.56098098,
        0.56100019, 0.56100019, 0.56100019, 0.56100019, 0.56100019,
        0.56100019, 0.56100019, 0.56100019, 0.56153689, 0.56153689,
        0.56153689, 0.56153689, 0.56153689, 0.56153689, 0.56153689,
        0.56153689, 0.56153689, 0.56153689, 0.56153689, 0.56153689,
        0.56153689, 0.56153689, 0.56153689, 0.56153747, 0.56153747,
        0.56153747, 0.56153747, 0.56153747, 0.56153747, 0.56153747,
        0.56153747, 0.56153747, 0.56153747, 0.56153747, 0.56153747,
        0.56153747, 0.56153747, 0.56153747, 0.56153747, 0.56153747,
        0.56153747, 0.56153747, 0.56153747, 0.56153747, 0.56153747,
        0.56153747, 0.56153747, 0.56153747, 0.56153747, 0.56153747,
        0.56153747, 0.56153747, 0.56153747, 0.56153747, 0.56153747,
        0.56153747, 0.56153747, 0.56153747, 0.55725495, 0.55725495,
        0.55721888, 0.55721888, 0.55721888, 0.55721888, 0.55721888,
        0.55721888, 0.55721888, 0.55721888, 0.55721888, 0.55818303,
        0.55678121, 0.56017594, 0.56017594, 0.56017594, 0.56017594,
        0.56017594, 0.56017594, 0.56017594, 0.56017594, 0.56017594,
        0.56017594, 0.56017594, 0.56017594, 0.55960685, 0.55960685,
        0.55960685, 0.55960685, 0.55960685, 0.55960685, 0.55960685,
        0.56643819, 0.57710531, 0.58263109, 0.58810689, 0.5966737 ,
        0.61432357, 0.61150142, 0.61760329, 0.62972435, 0.56726293,
        0.43744577, 0.47564653, 0.48299912, 0.64990792, 0.65113759,
        0.6510794 , 0.65175009, 0.65080489, 0.60105436, 0.39539715,
        0.3413659 , 0.28714813, 0.30081391, 0.30241954, 0.32695455,
        0.33266068, 0.29185039, 0.2994705 , 0.29856142, 0.2985614 ,
        0.2985614 , 0.2985614 , 0.2985614 , 0.2985614 , 0.2985614 ,
        0.2985614 , 0.2985614 , 0.2985614 , 0.2985614 , 0.2985614 ,
        0.2985614 , 0.2985614 , 0.2985614 , 0.2985614 , 0.2985614 ,
        0.2985614 , 0.2985614 , 0.2985614 , 0.2985614 , 0.29764627,
        0.29964028, 0.29964027, 0.29964027, 0.29964027, 0.29964027,
        0.29964027, 0.29964027],
       [0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.01234426, 0.10576678, 0.22198324,
        0.32966437, 0.45171857, 0.58777364, 0.7211764 , 0.77051056,
        0.8145679 , 0.85828384, 0.85590972, 0.86247118, 0.86058159,
        0.89332475, 0.98818116, 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 0.94093472, 0.8804191 ,
        0.8886052 , 0.81846082, 0.76088167, 0.66928209, 0.53313845,
        0.39542111, 0.23058339, 0.09544049, 0.00295322, 0.        ,
        0.00619936, 0.13030049, 0.33631845, 0.58353132, 0.89084691,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        , 1.        , 1.        , 1.        ,
        1.        , 1.        ]])}}
{'Payload': {'Cfg.MonitoredRoomDims': [0.5, 2.6, -4.0, -0.6, 0.8, 2.2], 'Cfg.Common.sensorOrientation.mountPlane': 'xy', 'Cfg.Common.sensorOrientation.transVec': [0.0, 0.0, 2.4], 'Cfg.imgProcessing.substractionMode': 6.0, 'Cfg.TargetProperties.MaxPersonsInArena': 2.0, 'Cfg.TargetProperties.StandingMaxHeight': 2.0, 'Cfg.TargetProperties.StandingMinHeight': 1.6, 'Cfg.TargetProperties.SittingMinHeight': 0.2, 'Cfg.TargetProperties.LyingMinHeight': 0.6, 'Cfg.TargetProperties.PersonRadius': 0.6, 'MPR.save_dir': '', 'MPR.read_from_file': 0.0, 'MPR.save_to_file': 0.0, 'MPR.save_image_to_file': 0.0, 'Cfg.OutputData.save_to_file': 0.0, 'Cfg.ExternalGUI.FilterImage.TH': 0.0, 'Cfg.ExternalGUI.FilterImage.numOfSd': 5.0, 'Cfg.PeopleCounter.inCarIsLocked': 0.0, 'Cfg.Zones.Beds': ''}, 'Type': 'COMMAND', 'ID': 'SET_PARAMS'}
{'Payload': {'PostureVector': ['Sitting', 'Sitting']}, 'Type': '', 'ID': 'JSON_DATA'}

```
