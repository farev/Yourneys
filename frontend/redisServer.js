const express = require("express");
const http = require("http");
const WebSocket = require("ws");
const redis = require("redis");

const REDIS_SERVER = "redis://localhost:6379";
const WS_PORT = 5173;

// Create redis client
const client = redis.createClient(REDIS_SERVER);

// Subscribe to the channel
client.subscribe("notifications");

// Create an Express app instance
const app = express();

// Create an HTTP server using the Express app instance
const server = http.createServer(app);

// Create a WebSocket server instance and attach it to the HTTP server
const websocketServer = new WebSocket.Server({ server });

server.listen(8000, () => {
    console.log("Websocket server started on port 5173");
});

websocketServer.on('connection', (socket) => {
    // Log a message when a new client connects
    console.log('client connected.');

    socket.on('message', (data) => {
        // Broadcast the message to all connected clients
        websocketServer.clients.forEach(function each(client) {
          if (client !== socket && client.readyState === WebSocket.OPEN) {
            console.log(client.socket)
            client.send(data.toString());
            console.log("message", data.toString())
            //console.log(data)
          }
        });
      });
  
      socket.on('notification', (data) => {
        // Broadcast the message to all connected clients
        websocketServer.clients.forEach(function each(client) {
          if (client !== socket && client.readyState === WebSocket.OPEN) {
            client.send(data.toString());
            console.log("notification", data.toString())
            console.log(data)
          }
        });
      });
  
      // Listen for WebSocket connection close events
      socket.on('close', () => {
        // Log a message when a client disconnects
        console.log('Client disconnected');
      });

    client.on('message', function(channel, msg){
        console.log(msg)
        socket.send(msg)
    }); 

  });

