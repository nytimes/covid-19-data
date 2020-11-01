const dataSource = require('./dataSource');

const State = {
  findOne(args) {
    if (!args?.select) return null;

    if (args.select.name) {
      const results = dataSource.filterByColumn('state', args.select.name);
      console.log('[rkd] results:', results);

      return results.length ? results[0] : null;
    }
  },
  query(args) {
    return [null, null];
  },
};

module.exports = State;
