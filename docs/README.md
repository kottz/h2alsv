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

The Vayyar sensor

## Front-end

The front-end is a web app written in React with a Node.js websocket server
connected to RabbitMQ. Since real-time updates is a top priority. 
## General Practices

The modules are all asynchronous and non-blocking. The sensor modules written
in python are all `asyncio` based. All modules use separate configuration files
written in TOML. 

## Git Workflow

The `develop` branch should be considered the main branch. `master` will only
be used for tested releases. When implementing a new feature make a new local
feature branch off of `develop`. When the feature is completed please rebase or
merge the changes onto the `develop` branch. Then push your changes to GitHub.
Please do not push to master. Do not merge `develop`onto master unless the
current develop commit has been thouroughly tested and documented.

All documentation should preferably be commited together with the featured code. 
No code will be accepted without proper documentation.

