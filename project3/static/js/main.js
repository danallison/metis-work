(function () {
  var urlInputEl = document.getElementById('url-input');
  var messageEl = document.getElementById('message-display');
  var propsTableEl = document.getElementById('properties-table-body');
  var responsesByURL = {};
  var currentURL = '';

  var fetchPredictions = function (url) {
    if (responsesByURL[url]) return Promise.resolve(responsesByURL[url]);
    return httpRequest('get', '/predict', {url: url}).then(function (response) {
      return responsesByURL[url] = response;
    });
  };

  var props = ['full_domain','domain','subdomain','path',
              'domain_total_chars','subdomain_total_chars','path_total_chars',
              'domain_entropy','subdomain_entropy','path_entropy',
              'https','path_ends_in_php','path_char_slash'];

  var updateMessage = function () {
    var url = _.trim(urlInputEl.textContent);
    console.log(url);
    if (urlFinder.isUrl(url)) {
      currentURL = url;
      fetchPredictions(url).then(function (response) {
        messageEl.innerHTML = [
          'prediction: ' + response.prediction,
          'domain-based prediction: ' + response.domain_prediction,
          'path-based prediction: ' + response.path_prediction
        ].join('<br/>');
        propsTableEl.innerHTML = props.map(function (key) {
          return '<tr><td>' + key + '</td><td>' + response.features[key] + '</td></tr>';
        }).join('');
      });
    } else {
      messageEl.innerHTML = 'Input must be a valid URL.'
    }
  };
  var debouncedUpdate = _.debounce(updateMessage, 1000);

  var progressBarHTML = '<div class="progress"><div class="indeterminate"></div></div>';
  var showProgressBar = function () {
    var url = _.trim(urlInputEl.textContent);
    if (url != currentURL && messageEl.innerHTML != progressBarHTML) {
      messageEl.innerHTML = progressBarHTML;
    }
  };
  var inputChangeHandler = _.flow(showProgressBar, debouncedUpdate);
  urlInputEl.addEventListener('paste', inputChangeHandler);
  urlInputEl.addEventListener('keyup', inputChangeHandler);

  urlInputEl.textContent = window.location.href;
  updateMessage();
})();
