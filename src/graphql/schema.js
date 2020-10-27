const { makeExecutableSchema } = require('apollo-server');
const gql = require('graphql-tag');
const chalk = require('chalk');

const ScalarTypes = require('./scalarTypes');
const Schemas = require('./app');

// ---

const logTitle = (num) =>
  console.log(
    chalk.bold.yellow(
      `\nCombining ${chalk.bold.gray('(' + num + ')')} app module${num === 1 ? '' : 's'}...`
    )
  );

const logListItem = (index, length, name, schema) =>
  console.log(
    `  ${index === length - 1 ? '└' : '├'}─ ${chalk.yellow(name)} `.padEnd(42) +
      chalk.dim.gray('| ') +
      chalk.cyan('•'.repeat(Object.keys(schema.resolvers?.Query || {}).length)) +
      chalk.magenta('•'.repeat(Object.keys(schema.resolvers?.Mutation || {}).length))
  );

// ---

const rootSchema = {
  _Root: {
    typeDefs: gql`
      type Query {
        _empty: String
      }
    `,
    resolvers: {
      Query: {
        _empty: () => null,
      },
    },
  },
};

function combineSchemas(schemasArray) {
  const schemas = schemasArray.map((schema) => Object.entries(schema)).flat();

  let index = 0;
  const combined = schemas.reduce(
    (output, [name, schema]) => {
      if (schema.appModule) logListItem(index, schemas.length, name, schema);
      if (schema.typeDefs) output.typeDefs.push(schema.typeDefs);
      if (schema.resolvers) output.resolvers.push(schema.resolvers);
      index++;
      return output;
    },
    { typeDefs: [], resolvers: [] }
  );

  return makeExecutableSchema(combined);
}

logTitle(Object.keys(Schemas).length);

module.exports = {
  schema: combineSchemas([rootSchema, ScalarTypes, Schemas]),
};
