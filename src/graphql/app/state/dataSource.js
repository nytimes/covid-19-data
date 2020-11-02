const fs = require('fs');
const path = require('path');

const CsvData = require('../../utils/CsvData');

const states = new CsvData({
  csvFile: 'processed/us-states.csv',
  idExtractor: (getCell) => {
    return getCell('name').toLowerCase().replace(' ', '-');
  },
});

module.exports = states;
