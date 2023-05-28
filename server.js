const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const { exec } = require('child_process');


io.sockets.on('connection', function(socket) {
	console.log('User connected')

    socket.on('message', function(data) {
        console.log(data)
        io.emit('respond', data);
    });

    // Handle run script request
    socket.on('run_script', (jsonData) => {
    // console.log('Received run_script request');
    console.log('Received run_script request with JSON data:', jsonData);
    console.log(jsonData.hours)
    // const parsedData = JSON.parse(jsonData);

    // Execute the Python script as a child process
    exec(`python main.py --hours ${jsonData.hours} --genre "${jsonData.genre}" --mood "${jsonData.mood}" --token "${jsonData.access_token}"`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error.message}`);
        return;
      }
      console.log('script response!')
      console.log(stdout)
      // Emit the script response to the client
      socket.emit('script_response', stdout);
    })
    });

    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

const server = http.listen(5000, function() {
    console.log('Running on port 5000');
});
