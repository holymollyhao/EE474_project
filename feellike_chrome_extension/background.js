// // Get reference to background page.
// const bgPage = chrome.extension.getBackgroundPage();
// // Sign in with popup, typically attached to a button click.
// bgPage.signInWithPopup();

chrome.identity.getAuthToken({ interactive: true }, function (token) {
  // Use the token.
  console.log(token);
  chrome.storage.sync.set({ access_token: token });
  // sendResponse({ access_token: token });
});

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "getAccessToken") {
    chrome.storage.sync.get("access_token", function (data) {
      var accessToken = data.access_token;
      sendResponse({ access_token: accessToken });
    });
    return true; // To indicate that sendResponse will be called asynchronously
  }
});
