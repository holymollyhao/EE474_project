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
        access_token: token,
      };

      var socket = io.connect("http://server36.mli.kr:5000/");
      socket.on("connect", function () {
        socket.emit("run_script", jsonData);
      });

      socket.on("script_response", function (response) {
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
  }
});
