const { makeExecutableSchema } = require('apollo-server');
const { applyMiddleware } = require('graphql-middleware');
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

function applyLogging(resolver) {
  return async (root, args, ctx, info) => {
    const operationType = info.operation.operation;
    const operationColor = operationType === 'query' ? chalk.blue : chalk.magenta;
    const operationName = info.operation.name.value;

    console.log(`\n${operationColor(operationType)} ${chalk.cyan(operationName)}`);
    console.log(`${operationColor('args')}`);
    console.log(chalk.gray(JSON.stringify(args, null, 2)));

    return resolver(root, args, ctx, info);
  };
}

function applyLoggingToQueryResolvers(resolvers) {
  if (!resolvers.Query) {
    return resolvers;
  }

  return {
    ...resolvers,
    Query: Object.fromEntries(
      Object.entries(resolvers.Query).map(([name, resolverFn]) => {
        return [name, applyLogging(resolverFn)];
      })
    ),
  };
}

function combineSchemas({ schemas, options = {} }) {
  logTitle(Object.keys(Schemas).length);
  const schemasFlat = schemas.map((schema) => Object.entries(schema)).flat();

  let index = 0;
  const combined = schemasFlat.reduce(
    (output, [name, schema]) => {
      if (schema.appModule) logListItem(index, schemasFlat.length, name, schema);
      if (schema.typeDefs) output.typeDefs.push(schema.typeDefs);
      if (schema.resolvers)
        output.resolvers.push(
          options.enableLogging ? applyLoggingToQueryResolvers(schema.resolvers) : schema.resolvers
        );
      index++;
      return output;
    },
    { typeDefs: [], resolvers: [] }
  );

  return applyMiddleware(makeExecutableSchema(combined));
}

function makeAppSchema(options) {
  return combineSchemas({
    options,
    schemas: [rootSchema, ScalarTypes, Schemas],
  });
}

module.exports = {
  makeAppSchema,
};
