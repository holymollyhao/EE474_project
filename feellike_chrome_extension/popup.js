// Dark Mode toggle functionality
const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)");
const body = document.querySelector("body");
const container = document.querySelector(".container");
const labels = document.querySelectorAll("label");
const inputs = document.querySelectorAll("input");
const buttons = document.querySelectorAll(".button");

function toggleDarkMode() {
  body.classList.toggle("dark-mode");
  container.classList.toggle("dark-mode");

  labels.forEach((label) => label.classList.toggle("dark-mode"));
  inputs.forEach((input) => input.classList.toggle("dark-mode"));
  buttons.forEach((button) => button.classList.toggle("dark-mode"));
}

function setDarkModeAccordingToSystemPreference() {
  if (prefersDarkMode.matches) {
    toggleDarkMode();
  }
}

setDarkModeAccordingToSystemPreference();

var hours = document.getElementById("hours");
var mood = document.getElementById("mood");
var genre = document.getElementById("genre");
var generate_button = document.getElementById("generateButton");

var goback_button = document.getElementById("goBackButton");
var goback2_button = document.getElementById("goBack2Button");

var create_button = document.getElementById("createButton");
var createvideo_button = document.getElementById("createVideoButton");
var createplaylist_button = document.getElementById("createPlaylistButton");

chrome.runtime.sendMessage({ message: "" });

// if previous value from chrome stroage exits run the follwoing function:
chrome.storage.local.get(["playlist", "image"], function (result) {
  console.log("playlist value currently is ");
  console.log(result);
  if (result.playlist != null) {
    var spinnerContainer = document.getElementById("spinnerContainer");
    var playlistForm = document.getElementById("playlistForm");

    spinnerContainer.classList.remove("hidden");
    playlistForm.classList.add("hidden");

    console.log("musiclist is :");
    console.log(result.playlist);
    displayResponse(result.playlist);
    displayImage(result.image);
  }
});

generate_button.onclick = function () {
  var date = new Date();
  // store date value to chrome storage
  chrome.storage.local.set({ date: date.toISOString() });
  chrome.storage.local.set({ hours: hours.value });
  chrome.storage.local.set({ mood: mood.value });
  chrome.storage.local.set({ genre: genre.value });

  const jsonData = {
    hours: hours.value,
    mood: mood.value,
    genre: genre.value,
    date: date.toISOString(),
  };
  chrome.runtime.sendMessage({ message: "send_to_server", jsonData: jsonData });

  var spinnerContainer = document.getElementById("spinnerContainer");
  var playlistForm = document.getElementById("playlistForm");

  spinnerContainer.classList.remove("hidden");
  playlistForm.classList.add("hidden");
};

goback_button.onclick = function () {
  var playlistForm = document.getElementById("playlistForm");
  var playlistContainer = document.getElementById("playlistContainer");
  var spinnerContainer = document.getElementById("spinnerContainer");

  // Show the playlist container
  playlistForm.classList.remove("hidden");
  playlistContainer.classList.add("hidden");
  spinnerContainer.classList.add("hidden");

  // restore original image
  var imageContainer = document.getElementById("imageContainer");
  imageContainer.src = "media/feel_like.png";
  imageContainer.style.borderRadius = "50%";
  imageContainer.style.width = "160px";
  imageContainer.style.height = "160px";

  // remove playlist from local storage
  chrome.storage.local.remove(["playlist", "image"], function () {
    console.log("removed playlist and image!");
  });
};

goback2_button.onclick = function () {
  var playlistForm = document.getElementById("playlistForm");
  var playlistContainer = document.getElementById("playlistContainer");
  var spinnerContainer = document.getElementById("spinnerContainer");

  // Show the playlist container
  playlistForm.classList.remove("hidden");
  playlistContainer.classList.add("hidden");
  spinnerContainer.classList.add("hidden");

  // restore original image
  var imageContainer = document.getElementById("imageContainer");
  imageContainer.src = "media/feel_like.png";
  imageContainer.style.borderRadius = "50%";
  imageContainer.style.width = "160px";
  imageContainer.style.height = "160px";

  // remove playlist from local storage
  chrome.storage.local.remove(["playlist", "image"], function () {
    console.log("removed playlist and image!");
  });
};

create_button.onclick = function () {
  var button1 = document.getElementById("button1");
  var button2 = document.getElementById("button2");

  button1.style.display = "none";
  button2.style.display = "flex";
};

createvideo_button.onclick = function () {
  // const nonDeletedItems = Array.from(
  //   document.querySelectorAll(".playlist-item")
  // ).map((item) => item.querySelector(".title").textContent);

  // read from chrome storage date value
  chrome.storage.local.get(
    ["date", "hours", "mood", "genre", "playlist"],
    function (result) {
      console.log(result);

      const jsonData = {
        hours: result.hours,
        mood: result.mood,
        genre: result.genre,
        musicArray: result.playlist,
        date: result.date,
      };
      // Perform the action with the non-deleted items list
      // For example, send the list to the server
      chrome.runtime.sendMessage({
        message: "create_video",
        jsonData: jsonData,
      });
    }
  );
};

createplaylist_button.onclick = function () {
  // const nonDeletedItems = Array.from(
  //   document.querySelectorAll(".playlist-item")
  // ).map((item) => item.querySelector(".title").textContent);

  chrome.storage.local.get(
    ["date", "hours", "mood", "genre", "playlist"],
    function (result) {
      console.log(result);

      const jsonData = {
        hours: result.hours,
        mood: result.mood,
        genre: result.genre,
        musicArray: result.playlist,
        date: result.date,
      };
      // Perform the action with the non-deleted items list
      // For example, send the list to the server
      chrome.runtime.sendMessage({
        message: "create_playlist",
        jsonData: jsonData,
      });
    }
  );

  // const jsonData = {
  //   hours: hours.value,
  //   mood: mood.value,
  //   genre: genre.value,
  //   musicArray: nonDeletedItems,
  // };
  // // Perform the action with the non-deleted items list
  // // For example, send the list to the server
  // console.log(nonDeletedItems);
  // chrome.runtime.sendMessage({
  //   message: "create_playlist",
  //   jsonData: jsonData,
  // });
};

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log(request);
  if (request.message === "display_response") {
    // change a musiclist of [Object] to [String]
    musiclist = request.musiclist.map((item) => item.title);
    // musiclist = request.musiclist;
    image = request.image;
    console.log("received display response");
    chrome.storage.local.set({ ["playlist"]: musiclist });
    chrome.storage.local.set({ ["image"]: image });

    displayResponse(musiclist);
    displayImage(image);
  }
});

function displayImage(image) {
  var imageContainer = document.getElementById("imageContainer");
  var image_src = "data:image/png;base64, ";
  image_src += image;

  imageContainer.src = image_src;
  imageContainer.style.borderRadius = "0%";
  imageContainer.style.width = "100%";
  imageContainer.style.height = "100%";
}

function displayResponse(playlist) {
  var playlistContainer = document.getElementById("playlistContainer");
  var playlistElement = document.getElementById("playlist");
  var spinnerContainer = document.getElementById("spinnerContainer");
  console.log("running displayResponse");
  console.log("playlist is :");
  console.log(playlist);

  // Clear any previous playlist items
  playlistElement.innerHTML = "";

  playlist.forEach(function (song) {
    const playlistItem = document.createElement("div");
    playlistItem.className = "playlist-item";

    const title = document.createElement("div");
    title.className = "title";
    title.textContent = song;
    playlistItem.appendChild(title);

    // Inside the playlist.forEach loop
    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button";
    // deleteButton.textContent = "Delete";
    playlistItem.appendChild(deleteButton);

    const img = new Image();
    img.src = "media/delete.png";
    deleteButton.appendChild(img);

    // Event listener for delete button
    deleteButton.addEventListener("click", function () {
      // Remove the corresponding playlist item from the DOM
      console.log("deleting array item: " + playlistItem.title);
      playlistContainer.removeChild(playlistItem);

      const nonDeletedItems = Array.from(
        document.querySelectorAll(".playlist-item")
      ).map((item) => item.querySelector(".title").textContent);
      chrome.storage.local.set({ ["playlist"]: nonDeletedItems });
    });

    const playlistContainer = document.getElementById("playlist");
    playlistContainer.appendChild(playlistItem);
  });

  // Show the playlist container
  playlistContainer.classList.remove("hidden");
  spinnerContainer.classList.add("hidden");
}
