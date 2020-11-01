const fs = require('fs');
const path = require('path');

const CsvData = require('../../utils/CsvData');

const states = new CsvData('processed/us-states.csv');

module.exports = states;
