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
The vayyar sensor has two different kind of payloads, the binary data that contains locationMatrix, NumOfPeople and breathingMatrix. Then we have the json data that contains the postureVector.

```javascript
{   'event_type': 'data',
    'payload': {   'ID': 'BINARY_DATA',
                   'Payload': {   'BreathingMatrix': [   [   0.10735835116050418,
                                                             0.10911491495840786,
                                                             0.10978676026641476,
                                                             0.10983348947444471,
                                                             0.10982685857733071,
                                                             0.1098109326868017,
                                                             0.10981138407456043,
                                                             0.1098295257260089,
                                                             0.1098114387495075,
                                                             0.10981639078335431,
                                                             0.11082160638563182,
                                                             0.11081930660766792,
                                                             0.11081903648580443,
                                                             0.11082108538830487,
                                                             0.11082108538830487,
                                                             0.11105403874089526,
                                                             0.11105403874089526,
                                                             0.11105403874089526,
                                                             0.11137280607348282,
                                                             0.13890419679986854,
                                                             0.13890419679986854,
                                                             0.13890419679986854,
                                                             0.13890419679986854,
                                                             0.13890419679986854,
                                                             0.12153202479780217,
                                                             0.12647958588950503,
                                                             0.1264830308977246,
                                                             0.1207487583977393,
                                                             0.1207490596884701,
                                                             0.12074909906889625,
                                                             0.12074897907818949,
                                                             0.12074897907818949,
                                                             0.12074897907818949,
                                                             0.12365910876274466,
                                                             0.16831199254431012,
                                                             0.2075846398510497,
                                                             0.3557259525260251,
                                                             0.5104561297481678,
                                                             0.6883281668813455,
                                                             0.5035719451237843,
                                                             0.5381543646977007,
                                                             0.5907988142611411,
                                                             0.5867723801877828,
                                                             0.6110240246080318,
                                                             0.605189930292446,
                                                             0.6163680502622613,
                                                             0.6048644662395108,
                                                             0.6095936971861693,
                                                             0.6190516020935086,
                                                             0.591565503402719,
                                                             0.5954259105173485,
                                                             0.5792988235810175,
                                                             0.6064215422853407,
                                                             0.5677852089405337,
                                                             0.532340503942093,
                                                             0.536328028361754,
                                                             0.4485573210633948,
                                                             0.4780447282718631,
                                                             0.5473700134378015,
                                                             0.5947394202767997,
                                                             0.6464312477185159,
                                                             0.6484292257170439,
                                                             0.6429706250693434,
                                                             0.6790073992952801,
                                                             0.6653661000188824,
                                                             0.6632058731686346,
                                                             0.6452236435889795,
                                                             0.6638630103791583,
                                                             0.6663600693063234,
                                                             0.6627825505528693,
                                                             0.6476310163091643,
                                                             0.6681146684564714,
                                                             0.6502952451974502,
                                                             0.6493021683664346,
                                                             0.6624587337236718,
                                                             0.6336643967603433,
                                                             0.6554285171027483,
                                                             0.6958105740428153,
                                                             0.6781786358835886,
                                                             0.668886448382483,
                                                             0.6820702508100058,
                                                             0.6886144404622179,
                                                             0.6816953297065123,
                                                             0.671577070023077,
                                                             0.7026836807714218,
                                                             0.6765219661309387,
                                                             0.6993567226670792,
                                                             0.66818249439534,
                                                             0.6505819010482643,
                                                             0.6748286250843445,
                                                             0.6617969938081458,
                                                             0.7328660833653906,
                                                             0.6471556176833084,
                                                             0.68260464224846,
                                                             0.6769111480059251,
                                                             0.6650036008673987,
                                                             0.6477344368466544,
                                                             0.661315762478927,
                                                             0.6753560378656283,
                                                             0.6901595857545573,
                                                             0.5950509595781003,
                                                             0.5761230424349919,
                                                             0.6359856169436657,
                                                             0.6190200480215795,
                                                             0.6042400127531978,
                                                             0.616996669430532,
                                                             0.6242122618916486,
                                                             0.6230506639462685,
                                                             0.6209129383076315,
                                                             0.615670271879365,
                                                             0.6119026439568864,
                                                             0.6190956465053634,
                                                             0.6101509359555639,
                                                             0.6051126805800615,
                                                             0.5784444771151368,
                                                             0.5663566545813954,
                                                             0.5822063587138357,
                                                             0.5549792752885473,
                                                             0.5710326042000209,
                                                             0.54129336757313,
                                                             0.5395803009311825,
                                                             0.6004371470857528,
                                                             0.5949341108476278,
                                                             0.5930426313390493,
                                                             0.5930426313390493,
                                                             0.5930426313390493,
                                                             0.5930426313390493,
                                                             0.5930426313390493,
                                                             0.5930426313390493,
                                                             0.5930426313390493,
                                                             0.5930426313390493,
                                                             0.6016154755685175,
                                                             0.6031967383198915,
                                                             0.6031620415599048,
                                                             0.6032125607777616,
                                                             0.5994437377167664,
                                                             0.5991062810784216,
                                                             0.5991270408138716,
                                                             0.5990579282663532,
                                                             0.6001938117058742,
                                                             0.5991303564300445,
                                                             0.5961415608120122,
                                                             0.5965181770933746,
                                                             0.5965164678343412,
                                                             0.5966019972729574,
                                                             0.5964830556227929,
                                                             0.5963151445416401,
                                                             0.5965698746673234,
                                                             0.5961463295904863,
                                                             0.5965858648385045,
                                                             0.5965870403081605,
                                                             0.5913799479401638,
                                                             0.5889902990557849,
                                                             0.587870212685656,
                                                             0.5884038025768032,
                                                             0.5856091362949645]],
                                  'LocationMatrix': [   [   0.9887076864178574,
                                                            -0.7667981337610865,
                                                            1.1092462180147535]],
                                  'NumOfPeople': 1.0}},
    'sensor_type': 'vayyar',
    'time': '2020-03-10T11:01:38.810875'}

{   'event_type': 'data',
    'payload': {   'ID': 'JSON_DATA',
                   'Payload': {'PostureVector': ['Sitting', 'NA', 'NA', 'NA']},
                   'Type': ''},
    'sensor_type': 'vayyar',
    'time': '2020-03-10T11:06:53.736745'} 

```
