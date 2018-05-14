(function () {

  var getCSV = function (path) {
    return new Promise(function (resolve) {
      d3.csv(path, function (err, data) {
        if (err) throw err;
        _.each(data, function (row) {
          _.each(row, function (cell, column) {
            row[column] = +cell;
          });
        })
        resolve(data);
      });
    });
  }

  var percentileDataPromise = Promise.all([
    getCSV('static/phishing_percentiles.csv'),
    getCSV('static/nonphishing_percentiles.csv')
  ]);

  var getData = function () { return percentileDataPromise; };

  var getRank = function (features) {
    return getData().then(function (percentiles) {
      var rank = {};
      _.each(percentiles, function (p, i) {
        _.each(p, function (row) {
          _.each(features, function (value, column) {
            // if (rank[column]) return;
            if (_.isNumber(row[column]) && value > row[column]) {
              rank[column] || (rank[column] = []);
              rank[column][i] = row.percentile;
            }
          });
        });
      });
      return rank;
    });
  };

  window.getRank = getRank;

})();
