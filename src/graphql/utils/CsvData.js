const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

// :: Utilities that need a better home
// ✂️ ------------------------------------------------
const COLUMN_VALUE_PARSERS = {
  Unknown: (value) => value,
  String: (value) => value.toString(),
  Int: (value) => parseInt(value, 10),
  Date: (value) => new Date(value),
};

const logPrefix = '[CsvData] ';
const log = {
  title: (value) => console.log(chalk.magenta(logPrefix) + chalk.magenta.bold(value)),
  tableHeader: (label, length) => {
    console.log();
    console.log(chalk.magentaBright(label), chalk.magenta(`(${length})`));
    console.log(chalk.dim.magenta('='.repeat(40)));
  },
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

const swapObjectKeysAndValues = (object) =>
  Object.fromEntries(Object.entries(object).map(([key, value]) => [value, key]));

const splitRows = (rows) => rows.split('\r\n');
const splitCols = (row) => Object.freeze(row.split(','));
const splitCsv = (csv) => splitRows(csv).map(splitCols);
// ✂️ ------------------------------------------------

class CsvData {
  constructor({ csvFile, idExtractor }) {
    console.log(chalk.magenta.bold('new CsvData()'), csvFile);
    this.csvFile = csvFile;
    this.idExtractor = idExtractor;

    this.readFile();
  }

  readFile() {
    const fullCsvPath = path.join(process.cwd(), this.csvFile);

    log.title('readCsv()');
    const csv = fs.readFileSync(fullCsvPath, { encoding: 'utf-8' });

    const allRows = splitCsv(csv);

    // Process header row/columns
    const { colNames, colTypes, colValueParsers } = allRows.shift().reduce(
      (output, headerCellValue) => {
        const [colName, colType = 'Unknown'] = headerCellValue.split(':');

        // Process column name
        const colNameClean = toCamel(colName);
        output.colNames.push(
          (!!this.renameColumns && this.renameColumns[colNameClean]) || colNameClean
        );

        // Process column type
        const colValueParser = COLUMN_VALUE_PARSERS[colType];
        if (colType === 'Unknown' || !colValueParser) {
          console.log(chalk.yellow(`⚠️  [CsvData] Unknown column type in "${headerCellValue}"`));
        }
        output.colTypes.push(colType);
        output.colValueParsers.push(colValueParser);

        return output;
      },
      { colNames: [], colTypes: [], colValueParsers: [] }
    );

    this.cols = arrayToObject(colNames);
    this.colIndexes = swapObjectKeysAndValues(this.cols);
    this.colValueParsers = colValueParsers;
    this.rows = Object.freeze(
      allRows.map((row) => row.map((cellValue, index) => this.colValueParsers[index](cellValue)))
    );

    // Log column definitions ---
    log.tableHeader('Columns', colNames.length);
    const longestColName = colNames.reduce((longest, current) => {
      return current.length > longest.length ? current : longest;
    }, '');
    colNames.forEach((colName, index) => {
      const separator = chalk.dim.magenta(' | ');
      const paddedColName = colName.padEnd(longestColName.length + 2, ' ');

      log.value(
        [index, paddedColName, colTypes[index]]
          .map((string) => chalk.magentaBright(string))
          .join(separator)
      );
    });

    log.tableHeader('Rows', this.rows.length);
    log.value(this.rows[0]);
    // // Generate a dict of column values for faster searching later
    // this.colValues = arrayToObject(headerRow, () => []);
    // this.rows.forEach((row, rowIndex) => {
    //   row.forEach((value, index) => {
    //     const colName = headerRow[index];
    //     this.colValues[colName].push({ index: rowIndex, value });
    //   });
    // });
  }

  getRowId(row) {
    return this.idExtractor((colNameOrIndex) => this.getCell(row, colNameOrIndex));
  }

  getColumnName(index) {
    return this.colIndexes[index];
  }

  getColumnIndex(nameOrIndex) {
    if (typeof nameOrIndex === 'string') {
      return this.cols[nameOrIndex];
    }

    return nameOrIndex;
  }

  getRow(index) {
    return this.rows[index];
  }

  getCell(rowOrRowIndex, colNameOrIndex) {
    const row = Array.isArray(rowOrRowIndex) ? rowOrRowIndex : this.rows[rowOrRowIndex];
    const col = this.getColumnIndex(colNameOrIndex);
    return row[col];
  }

  getObjectFromRow(
    row,
    { appendId = true, includeColumns, excludeColumns, renameColumns = {} } = {}
  ) {
    if (row.length !== Object.keys(this.cols).length) {
      throw new Error('Number of row values and columns are different');
    }

    // Return an object where keys are column names, values are cell values
    const entries = row
      .map((value, index) => {
        const colName = this.getColumnName(index);
        const colRenamed = renameColumns[colName] || colName;
        console.log('[rkd] colRenamed:', colRenamed);
        const entry = [colRenamed, value];

        if (includeColumns?.length) {
          return includeColumns.includes(colName) ? entry : null;
        }

        if (excludeColumns?.length) {
          return !excludeColumns.includes(colName) ? entry : null;
        }

        return entry;
      })
      .filter((entry) => !!entry);

    if (appendId) {
      entries.unshift(['id', this.getRowId(row)]);
    }

    const rowObject = Object.fromEntries(entries);

    console.log('[rkd] 🔸 rowObject:', rowObject);
    return rowObject;
  }

  getObjectsFromRows(rows) {
    return rows.map((row) => this.getObjectFromRow(row));
  }

  // Find rows that match a given column value
  filterByColumn(colName, value, { limit, reverseSort = false } = {}) {
    log.title('filterByColumn');
    log.value('colName:', chalk.green(`"${colName}"`));
    log.value('value:', chalk.green(`"${value}"`));
    log.value('options.limit:', chalk.yellow(limit));
    log.value('options.reverseSort:', chalk.yellow(reverseSort));
    const output = [];
    const isLimitReached = () => limit >= 1 && output.length >= limit;

    for (
      let rowIndex = reverseSort ? this.rows.length - 1 : 0;
      reverseSort ? rowIndex > 0 : rowIndex < this.rows.length;
      reverseSort ? rowIndex-- : rowIndex++
    ) {
      if (this.getCell(rowIndex, this.cols[colName]) === value) {
        output.push(this.getRow(rowIndex));
      }

      if (isLimitReached()) {
        break;
      }
    }

    console.log('[rkd] output.length:', output.length);
    return output;
  }
}

module.exports = CsvData;
