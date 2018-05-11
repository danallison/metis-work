var urlInputEl = document.getElementById('url-input');

var fetchPredictions = _.debounce(function (url) {
  httpRequest('get', '/predict', {url: url}).then(function (response) {
    console.log(response)
  })
}, 500);
urlInputEl.addEventListener('keyup', function (e) {
  console.log(urlInputEl.textContent);
  if (urlFinder.isUrl(urlInputEl.textContent)) {
    fetchPredictions(urlInputEl.textContent);
  }
});
