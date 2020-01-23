const WebSocket = require('ws')
const wss = new WebSocket.Server({ port: 3030 });
const fs = require('fs');
const toml = require('toml');

const config = toml.parse(fs.readFileSync('./config.toml', 'utf-8'));
const rmq_conf = config.rabbitmq;

var amqp = require('amqplib/callback_api');
var amqpConn = null;

function start() {
	let amqp_string = "amqp://"+
		rmq_conf['username']+
		":"+
		rmq_conf['password']+
		"@"+
		rmq_conf['host'];
  	amqp.connect(amqp_string, function(err, conn) {
    if (err) {
      console.error("[AMQP]", err.message);
      return setTimeout(start, 1000);
    }
    conn.on("error", function(err) {
      if (err.message !== "Connection closing") {
        console.error("[AMQP] conn error", err.message);
      }
    });
    conn.on("close", function() {
      console.error("[AMQP] reconnecting");
      return setTimeout(start, 1000);
    });
    console.log("[AMQP] connected");
    amqpConn = conn;
    whenConnected();
  });
}

function whenConnected() {
//  startPublisher();
  startWorker();
}

function startWorker() {
  amqpConn.createChannel(function(err, ch) {
    if (closeOnErr(err)) return;
    ch.on("error", function(err) {
      console.error("[AMQP] channel error", err.message);
    });
    ch.on("close", function() {
      console.log("[AMQP] channel closed");
    });

    //ch.prefetch(10);
    ch.assertQueue("test", { durable: true, maxLength: 100 }, function(err, _ok) {
      if (closeOnErr(err)) return;
      ch.consume("test", processMsg, { noAck: false });
      console.log("Worker is started");
    });
function processMsg(msg) {
  work(msg, function(ok) {
    try {
      if (ok)
        ch.ack(msg);
      else
        ch.reject(msg, true);
    } catch (e) {
      closeOnErr(e);
    }
  });
}
  });
}

function closeOnErr(err) {
  if (!err) return false;
  console.error("[AMQP] error", err);
  amqpConn.close();
  return true;
}

function work(msg, cb) {
	wss.clients.forEach(function each(client) {
		if (client.readyState === WebSocket.OPEN) {
			client.send(msg.content.toString());
		}
	});

  console.log("Message received: ", msg.content.toString());
  cb(true);
}

//Send an initial connected message on connect
wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
	ws.send('yoyo');
  });

  ws.send('connected to wss server');
});

start();
