const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const logPrefix = '[CsvData] ';
const log = {
  title: (value) => console.log(chalk.magenta(logPrefix) + chalk.magentaBright(value)),
  value: (...args) => console.log(chalk.magenta.dim('--> ') + chalk.magenta(...args)),
};

const toCamel = (string) => {
  return string.replace(/([-_][a-z])/gi, ($1) => {
    return $1.toUpperCase().replace('-', '').replace('_', '');
  });
};
const arrayToObject = (array, valueSetter) =>
  Object.fromEntries(
    array.map((item, index) => [item, valueSetter ? valueSetter(item, index) : index])
  );

const splitRows = (rows) => rows.split('\r\n');
const splitCols = (row) => Object.freeze(row.split(','));
const splitCsv = (csv) => splitRows(csv).map(splitCols);

class CsvData {
  constructor(csvFile) {
    console.log(chalk.magenta.bold('new CsvData()'), csvFile);
    this.csvFile = csvFile;

    this.readFile();
  }

  readFile() {
    const fullCsvPath = path.join(process.cwd(), this.csvFile);

    console.log(chalk.bold.magenta('readCsv()'));
    const csv = fs.readFileSync(fullCsvPath, { encoding: 'utf-8' });

    const allRows = splitCsv(csv);
    const headerRow = allRows.shift().map(toCamel);
    this.cols = arrayToObject(headerRow);
    this.rows = Object.freeze(allRows);

    console.log('this.cols:', this.cols);
    console.log('total rows: ', this.rows.length);

    // Generate a dict of column values for faster searching later
    this.colValues = arrayToObject(headerRow, () => []);
    this.rows.forEach((row, rowIndex) => {
      row.forEach((value, index) => {
        const colName = headerRow[index];
        this.colValues[colName].push({ index: rowIndex, value });
      });
    });
  }

  getRow(rowIndex) {
    return this.rows[rowIndex];
  }

  getCell(rowIndex, colNameOrIndex) {
    const col = typeof colNameOrIndex === 'string' ? this.cols[colNameOrIndex] : colNameOrIndex;
    return this.rows[rowIndex][col];
  }

  // Find rows that match a given column value
  filterByColumn(col, value, { limit } = {}) {
    log.title('filterByColumn');
    log.value('col:', chalk.green(`"${col}"`));
    log.value('value:', chalk.green(`"${value}"`));
    log.value('limit:', chalk.yellow(limit));
    const output = [];

    for (let rowIndex = 0; rowIndex < this.rows.length; rowIndex++) {
      if (this.getCell(rowIndex, this.cols[col]) === value) {
        output.push(this.getRow(rowIndex));
      }

      if (limit >= 1 && output.length >= limit) {
        break;
      }
    }

    console.log('[rkd] output.length:', output.length);
    return output;
  }
}

module.exports = CsvData;
