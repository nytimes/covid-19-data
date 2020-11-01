const dataSource = require('./dataSource');

const State = {
  deriveStatesFromRows(rows) {
    console.log('[rkd] dataSource.cols:', dataSource.cols);
    const output = [];

    console.log(dataSource.getObjectsFromRows(rows));
  },
  findOne(args) {
    if (!args?.select) return null;

    if (args.select.name) {
      const results = dataSource.filterByColumn('state', args.select.name);
      console.log('[rkd] results:', results);

      this.deriveStatesFromRows(results);
      console.log(dataSource.getObjectFromRow(results[0]));

      return results.length ? results[0] : null;
    }
  },
  query(args) {
    return [null, null];
  },
};

module.exports = State;
