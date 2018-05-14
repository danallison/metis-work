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
    if (urlFinder.isUrl(url)) {
      currentURL = url;
      fetchPredictions(url).then(function (response) {
        messageEl.innerHTML = [
          'overall phishy-ness: <b>' + _.round(response.prediction, 3) + '</b>',
          'phishy-ness of host: <b>' + _.round(response.domain_prediction, 3) + '</b>',
          'phishy-ness of path: <b>' + _.round(response.path_prediction, 3) + '</b>'
        ].join('<br/>');
        getRank(response.features).then(function (rank) {
          var sortedFeatures = _.sortBy(_.keys(response.features), function (key) {
            if (!rank[key]) return -Infinity;
            return -Math.abs(rank[key][0] - rank[key][1]);
          });
          propsTableEl.innerHTML = sortedFeatures.map(function (key) {
            if (!rank[key]) return '';
            var phishingPercentile = rank[key][0] || 0.99;
            var nonphishingPercentile = rank[key][1] || 0.99;
            var phishingFontSize = 'style="font-size:' + (10 + 36 * phishingPercentile) + 'px;' +
              'font-weight: ' + (phishingPercentile > nonphishingPercentile ? 500 : 300) + ';"';
            var nonphishingFontSize = 'style="font-size:' + (10 + 36 * nonphishingPercentile) + 'px;' +
              'font-weight: ' + (phishingPercentile < nonphishingPercentile ? 500 : 300) + ';"';
            return '<tr>' +
              '<td>' + key + '</td>' +
              '<td>' + response.features[key] + '</td>' +
              '<td '+ phishingFontSize + '>' + phishingPercentile + '</td>' +
              '<td '+ nonphishingFontSize + '>' + nonphishingPercentile + '</td>' +
            '</tr>';
          }).join('');
        });
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
