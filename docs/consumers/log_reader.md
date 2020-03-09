# Log Reader 
This module provides is reads logs from the log exchange in real-time.
It is intentionally kept basic since a proper logging platform (ELK,
Graylog etc.) will be deployed in the future.

## Starting the log reader

To start the log reader run:

```bash
python log_reader.py
```
Make sure you have a valid config file before starting. 

## Configuration
The module will look for a file named `config.toml` in the root directory.
RMQ settings are configured here.


The config file is structured as the example below.


```toml
[rabbitmq]
username = "my_username"
password = "my_password"
host = "my_host"
log_exchange = "log"
```