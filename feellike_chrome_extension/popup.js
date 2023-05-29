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
var generate_button = document.querySelector(".button");
chrome.runtime.sendMessage({ message: "" });

generate_button.onclick = function () {
  const jsonData = {
    hours: hours.value,
    mood: mood.value,
    genre: genre.value,
  };
  chrome.runtime.sendMessage({ message: "send_to_server", jsonData: jsonData });
};
