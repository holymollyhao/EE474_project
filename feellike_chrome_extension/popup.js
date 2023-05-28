var hours = document.getElementById("hours");
var mood = document.getElementById("mood");
var genre = document.getElementById("genre");
var generate_button = document.querySelector(".button");

// chrome.runtime.sendMessage({ method: "getToken" }, function (response) {
//   if (response && response.access_token) {
//     console.log("within get token!!");
//     console.log(response.data);
//   }
// });

generate_button.onclick = function () {
  chrome.storage.local.set({ hours: hours.value });
  chrome.storage.local.set({ mood: mood.value });
  // chrome.storage.local.set({ genre: genre.value });
  chrome.storage.local.set({ genre: genre.value }, function () {
    console.log("safely saved!");
  });

  chrome.storage.sync.get("access_token", function (data) {
    var accessToken = data.access_token;
    const jsonData = {
      hours: hours.value,
      mood: mood.value,
      genre: genre.value,
      access_token: accessToken,
    };
    console.log("jsonData is :");
    console.log(jsonData);
    var socket = io.connect("http://server36.mli.kr:5000/");
    socket.on("connect", function () {
      socket.emit("run_script", jsonData);
    });
    socket.on("script_response", function (response) {
      hours.value = "";
      mood.value = "";
      genre.value = "";
      alert(
        `Generate ${hours.value}-h playlist of ${mood.value} ${genre.value}!`
      );
      socket.close();
    });
  });
};
