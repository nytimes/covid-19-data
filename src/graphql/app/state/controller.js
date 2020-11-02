const dataSource = require('./dataSource');

const State = {
  createFromRow(row) {
    return dataSource.getObjectFromRow(row, {
      includeColumns: ['name', 'population', 'date', 'casesCumulative', 'deathsCumulative'],
      renameColumns: {
        date: 'mostRecentDataDate',
      },
    });
  },
  // deriveStatesFromRows(rows) {
  //   const output = {};

  //   rows.forEach((row) => {
  //     const rowId = dataSource.getRowId(row);

  //     // Create key for this state on output
  //     if (!output[rowId]) {
  //       output[rowId] = [];
  //     }

  //     output[rowId].push(this.createFromRow(row));
  //   });

  //   return output;
  // },
  findOne(args) {
    if (!args?.select) return null;

    if (args.select.name) {
      const result = dataSource
        .filterByColumn('name', args.select.name, { reverseSort: true, limit: 1 })
        .pop();

      console.log('[rkd] result:', result);

      const stateObject = this.createFromRow(result);
      console.log('stateObject:', stateObject);

      return stateObject;
    }
  },
  query(args) {
    return [null, null];
  },
};

module.exports = State;
