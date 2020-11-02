const fs = require('fs');
const path = require('path');

const CsvData = require('../../utils/CsvData');

const states = new CsvData({
  csvFile: 'processed/us-states.csv',
  renameColumns: {
    state: 'name',
  },
  idExtractor: (getCell) => {
    return getCell('name').toLowerCase().replace(' ', '-');
  },
});

module.exports = states;
