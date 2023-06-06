chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log(request);
  if (request.message === "send_to_server") {
    chrome.identity.getAuthToken({ interactive: true }, function (token) {
      console.log("token is :");
      console.log(token);

      const jsonData = {
        hours: request.jsonData.hours,
        mood: request.jsonData.mood,
        genre: request.jsonData.genre,
        datetime: request.jsonData.date,
        access_token: token,
      };

      var socket = io.connect("http://server36.mli.kr:5000/");
      socket.on("connect", function () {
        socket.emit("get_music_list", jsonData);
      });

      socket.on("connect_error", function (error) {
        console.error("Socket.IO connection error:", error);
        socket.close();
      });

      socket.on("get_music_list_response", function (response) {
        console.log(response);
        if (response.status == 1) {
          chrome.runtime.sendMessage({
            message: "display_response",
            musiclist: response.list_data,
            image: response.image,
          });
        } else {
          alert(
            `Music list & Cover image generation failed ㅠㅜ!\nPlease try again after some time...`
          );
        }
        socket.close();
      });
    });
  } else if (request.message === "create_playlist") {
    chrome.identity.getAuthToken({ interactive: true }, function (token) {
      console.log("token is :");
      console.log(token);

      const musicArray = request.jsonData;
      const jsonData = {
        hours: request.jsonData.hours,
        mood: request.jsonData.mood,
        genre: request.jsonData.genre,
        musicArray: request.jsonData.musicArray,
        access_token: token,
      };

      var socket = io.connect("http://server36.mli.kr:5000/");
      socket.on("connect", function () {
        socket.emit("create_playlist", jsonData);
      });

      socket.on("connect_error", function (error) {
        console.error("Socket.IO connection error:", error);
        socket.close();
      });

      socket.on("create_playlist_response", function (response) {
        if (response.status == 1) {
          alert(`Music uploaded!`);
        } else {
          alert(
            `Music upload failed ㅠㅜ!\nPlease try again after some time...`
          );
        }
        socket.close();
      });
    });
  } else if (request.message === "create_video") {
    chrome.identity.getAuthToken({ interactive: true }, function (token) {
      console.log("token is :");
      console.log(token);

      const musicArray = request.jsonData;
      const jsonData = {
        hours: request.jsonData.hours,
        mood: request.jsonData.mood,
        genre: request.jsonData.genre,
        musicArray: request.jsonData.musicArray,
        access_token: token,
        date: request.jsonData.date,
      };

      var socket = io.connect("http://server36.mli.kr:5000/");
      socket.on("connect", function () {
        socket.emit("create_video", jsonData);
      });

      socket.on("connect_error", function (error) {
        console.error("Socket.IO connection error:", error);
        socket.close();
      });

      socket.on("create_playlist_response", function (response) {
        if (response.status == 1) {
          alert(`PlaylistVideo uploaded!`);
        } else {
          alert(
            `PlaylistVideo upload failed ㅠㅜ!\nPlease try again after some time...`
          );
        }
        socket.close();
      });
    });
  }
});
