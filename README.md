# Human Health and Activity Lab Sensor Visualization
Projekt i kursen D0020E - Realtidsvisualisering av sensordata i Aktivitetslabbet på LTU

This project is developed as part of the D0020E course at LTU.

The Human Health and Activity Laboratory is a new research facility implemented
in 2018 at LTU. It is a smart home environment with numerous different sensors.
The goal is to create a modular system that collects and visualizes data from
different sensors in real-time. This repository contains different modules
that produce and consume data.

## Sensor Support

Currently the planned sensor support is

* Vayyar
* WideFind
* Z-wave (Kitchen Cabinets)

## Front-end

The front-end is a web app written in React with a Node.js websocket server
connected to RabbitMQ. Since real-time updates is a top priority. 
