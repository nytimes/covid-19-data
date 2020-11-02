const fs = require('fs');
const path = require('path');

const CsvData = require('../../utils/CsvData');

const extractIdFromName = (getCell) => {
  return getCell('name').toLowerCase().replace(' ', '-');
};
const statePopulationsCsvData = new CsvData({
  csvFile: 'processed/us-state-populations.csv',
  idExtractor: extractIdFromName,
});
const statePopulations = Object.fromEntries(statePopulationsCsvData.rows);

const statesCsvData = new CsvData({
  csvFile: 'processed/us-states.csv',
  rowIdExtractor: extractIdFromName,
  derivedColumns: [
    {
      name: 'population',
      valueCreator: (rowObject) => statePopulations[rowObject.name],
    },
  ],
});

module.exports = statesCsvData;
