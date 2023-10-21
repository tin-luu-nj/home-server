chrome.webNavigation.onBeforeNavigate.addListener(function(details) {
    if (details.url.startsWith('magnet:')) {
      console.log('User clicked on magnet link: ' + details.url);
      // Handle the magnet link here
    }
  });
  