# ws_server 
This module provides a websocket server which the web client connects to. The
server consumes data from RabbitMQ and forwards it to all connected websocket
clients. It is fully `asyncio` based. Configuration is done through a
`config.toml` file.

## Starting the server

To start the server run:

```bash
python ws_server.py
```
Make sure you have a valid config file before starting. 

## Configuration
The module will look for a file named `config.toml` in the root directory.
RMQ and websocket settings are configured here.


The config file is structured as the example below.


```toml
[rabbitmq]
username = "my_username"
password = "my_password"
host = "my_host"
sensor_exchange = "sensor_data"

[websocket]
ip = "0.0.0.0"
port = 3030
```

## Current Limitations

- Better queue management configuration possibilites will be added.
- Proper exception handling is not yet in place.
- Logging
