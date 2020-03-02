# Introduction

The goal of the project is to design a modular and easily expandable system
for producing and consuming sensor data.
## System Design

The overall system design is based on microservices connected through a
RabbitMQ message broker. Each sensor has its own producer module. The producers
send collected sensor data to the RMQ server.

The consumers visualize the data from the different sensors. From the Web UI it
is possible to view the data sent from each sensor. Each sensor also sends a
continous heartbeat to confirm connection to RMQ. The status of each sensor
module is visible from the Web UI. It should be simple for a user to view the
status of the entire system. All module logs are saved in a central database.

The figure below shows a graphical representation of the overall design.

![system design](../img/system_design.png)

No knowledge of the producer modules should be needed to create a new consumer.
The consumer simply connects to RabbitMQ and fetches data from the relevant
exchange.

Producers send sensor data to the `sensor_data` exchange in RabbitMQ. For a more
in-depth description on how to send and consume data see the 
[RabbitMQ](general/rabbitmq.md) page.

Guidelines on how to contribute can be found on the
[Developing a new Module](general/develop_new_module.md) page.

All data sent to RabbitMQ must adhere to the 
[h2alsv protocol](general/h2alsv_protocol.md).
