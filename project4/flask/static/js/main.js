(function () {
  var toQueryString = function (obj) {
    return Object.keys(obj).map(function (key) {
      var val = typeof obj[key] === 'string' ? obj[key] : JSON.stringify(obj[key]);
      return key + '=' + encodeURIComponent(val);
    }).join('&');
  };
  var inputEl = document.getElementById('description-input');
  var imageEl = document.getElementById('image-display');
  var progressBarContainerEl = document.getElementById('progress-container');
  var currentText = '';

  var updateImage = function () {
    var text = _.trim(inputEl.textContent);
    imageEl.src = '/predict?' + toQueryString({text: text})
    imageEl.style.display = 'block';
    progressBarContainerEl.innerHTML = '';
  };
  var debouncedUpdate = _.debounce(updateImage, 1000);
  var progressBarHTML = '<div class="progress"><div class="indeterminate"></div></div>';
  var showProgressBar = function () {
    var text = _.trim(inputEl.textContent);
    if (text != currentText && progressBarContainerEl.innerHTML != progressBarHTML) {
      progressBarContainerEl.innerHTML = progressBarHTML;
      imageEl.style.display = 'none';
    }
  };
  var inputChangeHandler = _.flow(showProgressBar, debouncedUpdate);
  inputEl.addEventListener('paste', inputChangeHandler);
  inputEl.addEventListener('keyup', inputChangeHandler);

  inputEl.textContent = imageEl.src.split('?text=')[1];
  updateImage();
})();
