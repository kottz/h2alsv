# Web UI

The main user interface is a responsive web app written in React with a Node.js
backend. By writing the app in React it is possible to easily separate the
sensors into different modules that can be developed separately. The app is
bootstrapped with Facebook's [create-react-app](https://create-react-app.dev). 

The Node.js backend provides a websocket server which the front-end is
connected to. The backend is connected to the RabbitMQ server and broadcasts
incoming messages over the websocket in real-time to all connected clients.





## Future improvements

* Change producer settings from the client front-end.

