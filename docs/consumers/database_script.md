# Database script
The database script is a consumer which sends the sensor data from the RabbitMQ server to the database. The script is using `Data Aggregator module` that implements the database APIs. The script also has an external `toml` config where you can change the connection and which data to forward to the database.

## Starting the database script

To start the database script run:

```bash
python database_script.py
```
The default behaviour for the script is to collect the data from all the sensor types and forward it to the database indefinetly (until terminated). The script also require the `Data Aggregator module` in the root directory to be able to run.

## Configuration
The script loads a config called `config_database_script.toml` in the root directory.

```toml
#Config for the database script
#0: all sensor data, 
#1: only vayyar data, 
#2: only widefind data, 
#3: only zwave data

[rabbitmq]
username = "username"
password = "password"
host = "host"
sensor_exchange = "sensor exchange"
log_exchange = "log exchange"
exchange_type = "exchange type"
sensor_type = 0

[database]
entrypoint = "entrypoint" 
username = "username"
password = "password"
startTime = "start time"
endTime = "end time"
type = "type"
label = "label"

[token]
expiration_time = expiration time
```