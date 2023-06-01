const express = require("express");
const app = express();
const http = require("http").Server(app);
const io = require("socket.io")(http);
const { exec } = require("child_process");

function parsePlaylist(stdout) {
  const regex = /title: (.*)/g;
  const matches = stdout.matchAll(regex);
  const playlist = [];

  for (const match of matches) {
    const title = match[1];
    const url = match[2];
    playlist.push({ title, url });
  }

  return playlist;
}

io.sockets.on("connection", function (socket) {
  console.log("User connected");

  // socket.on('message', function(data) {
  //     console.log(data)
  //     io.emit('respond', data);
  // });

  // Handle run script request
  socket.on("run_script", (jsonData) => {
    // console.log('Received run_script request');
    console.log("Received run_script request with JSON data:", jsonData);
    console.log(jsonData.hours);
    // const parsedData = JSON.parse(jsonData);

    // Execute the Python script as a child process
    exec(
      `python main.py --hours ${jsonData.hours} --genre "${jsonData.genre}" --mood "${jsonData.mood}" --token "${jsonData.access_token}"`,
      (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing Python script: ${error.message}`);
          socket.emit("script_response", { status: 0 });
          return;
        }
        console.log("script response!");
        console.log(stdout);
        // Emit the script response to the client
        socket.emit("script_response", { status: 1 });
      }
    );
  });

  socket.on("get_music_list", (jsonData) => {
    // console.log('Received run_script request');
    console.log("Received get_music_list request with JSON data:", jsonData);
    console.log(jsonData.hours);
    // const parsedData = JSON.parse(jsonData);

    // Execute the Python script as a child process
    exec(
      `python generate_music_list.py --hours ${jsonData.hours} --genre "${jsonData.genre}" --mood "${jsonData.mood}" --token "${jsonData.access_token}"`,
      (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing Python script: ${error.message}`);
          socket.emit("get_music_list_response", { status: 0 });
          return;
        }
        console.log("script response!");
        console.log("stdout!!!!!!!");
        console.log(stdout);
        console.log("\n\nparsing!!!!!!!");
        console.log(parsePlaylist(stdout));
        // Emit the script response to the client
        socket.emit("get_music_list_response", {
          status: 1,
          list_data: parsePlaylist(stdout),
        });
      }
    );
  });

  socket.on("create_playlist", (jsonData) => {
    // console.log('Received run_script request');
    console.log("Received create_playlist request with JSON data:", jsonData);
    // const parsedData = JSON.parse(jsonData);

      // create a string that can be passed into the python script, space separated, with quotes around each element of jsonData.musicArray
        let musicArrayString = "";
        for (let i = 0; i < jsonData.musicArray.length; i++) {
            musicArrayString += `"${jsonData.musicArray[i]}" `;
        }

    // Execute the Python script as a child process
    exec(
      `python create_playlist.py --hours ${jsonData.hours} --genre "${jsonData.genre}" --mood "${jsonData.mood}" --token "${jsonData.access_token}" --music_array ${musicArrayString}`,
      (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing Python script: ${error.message}`);
          socket.emit("create_playlist_response", { status: 0 });
          return;
        }
        console.log("script response!");
        console.log("stdout!!!!!!!");
        console.log(stdout);
        // Emit the script response to the client
        socket.emit("create_playlist_response", { status: 1 });
      }
    );
  });

  socket.on("create_video", (jsonData) => {
    // console.log('Received run_script request');
    console.log("Received create_video request with JSON data:", jsonData);
    // const parsedData = JSON.parse(jsonData);

      // create a string that can be passed into the python script, space separated, with quotes around each element of jsonData.musicArray
        let musicArrayString = "";
        for (let i = 0; i < jsonData.musicArray.length; i++) {
            musicArrayString += `"${jsonData.musicArray[i]}" `;
        }

    // Execute the Python script as a child process
    exec(
      `python create_video.py --hours ${jsonData.hours} --genre "${jsonData.genre}" --mood "${jsonData.mood}" --token "${jsonData.access_token}" --music_array ${musicArrayString}`,
      (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing Python script: ${error.message}`);
          socket.emit("create_playlist_response", { status: 0 });
          return;
        }
        console.log("script response!");
        console.log("stdout!!!!!!!");
        console.log(stdout);
        // Emit the script response to the client
        socket.emit("create_playlist_response", { status: 1 });
      }
    );
  });

  socket.on("disconnect", () => {
    console.log("User disconnected");
  });
});

const server = http.listen(5000, function () {
  console.log("Running on port 5000");
});
