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
var createplaylist_button = document.getElementById("createPlaylistButton");

chrome.runtime.sendMessage({ message: "" });

generate_button.onclick = function () {
  const jsonData = {
    hours: hours.value,
    mood: mood.value,
    genre: genre.value,
  };
  chrome.runtime.sendMessage({ message: "send_to_server", jsonData: jsonData });

  var spinnerContainer = document.getElementById("spinnerContainer");
  var playlistForm = document.getElementById("playlistForm");

  spinnerContainer.classList.remove("hidden");
  playlistForm.classList.add("hidden");
};

goBackButton.onclick = function () {
  var playlistForm = document.getElementById("playlistForm");
  var playlistContainer = document.getElementById("playlistContainer");
  var spinnerContainer = document.getElementById("spinnerContainer");

  // Show the playlist container
  playlistForm.classList.remove("hidden");
  playlistContainer.classList.add("hidden");
  spinnerContainer.classList.add("hidden");
};

createplaylist_button.onclick = function () {
  const nonDeletedItems = Array.from(
    document.querySelectorAll(".playlist-item")
  ).map((item) => item.querySelector(".title").textContent);

  const jsonData = {
    hours: hours.value,
    mood: mood.value,
    genre: genre.value,
    musicArray: nonDeletedItems,
  };
  // Perform the action with the non-deleted items list
  // For example, send the list to the server
  console.log(nonDeletedItems);
  chrome.runtime.sendMessage({
    message: "create_playlist",
    jsonData: jsonData,
  });
};
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log(request);
  if (request.message === "display_musiclist") {
    musiclist = request.musiclist;
    console.log("musiclist is :");
    console.log(musiclist);
    displayPlaylist(musiclist);
  }
});

function displayPlaylist(playlist) {
  var playlistContainer = document.getElementById("playlistContainer");
  var playlistElement = document.getElementById("playlist");
  var spinnerContainer = document.getElementById("spinnerContainer");

  // Clear any previous playlist items
  playlistElement.innerHTML = "";

  playlist.forEach(function (song) {
    const playlistItem = document.createElement("div");
    playlistItem.className = "playlist-item";

    const title = document.createElement("div");
    title.className = "title";
    title.textContent = song.title;
    playlistItem.appendChild(title);

    // Inside the playlist.forEach loop
    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button";
    deleteButton.textContent = "Delete";
    playlistItem.appendChild(deleteButton);

    // Event listener for delete button
    deleteButton.addEventListener("click", function () {
      // Remove the corresponding playlist item from the DOM
      playlistContainer.removeChild(playlistItem);
    });

    const playlistContainer = document.getElementById("playlist");
    playlistContainer.appendChild(playlistItem);
  });

  // Show the playlist container
  playlistContainer.classList.remove("hidden");
  spinnerContainer.classList.add("hidden");

  // Show the playlist container
}
