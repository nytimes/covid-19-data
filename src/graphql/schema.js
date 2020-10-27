const { makeExecutableSchema } = require('apollo-server');
const gql = require('graphql-tag');
const chalk = require('chalk');

const Schemas = require('./app');

const rootSchema = {
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
};

const logTitle = (num) =>
  console.log(
    chalk.bold.cyan(
      `\nCombining ${chalk.bold.gray('(' + num + ')')} app module${num === 1 ? '' : 's'}...`
    )
  );

function combineSchemas(rootSchema, schemas) {
  const typeDefs = [rootSchema.typeDefs];
  const resolvers = [rootSchema.resolvers];
  const schemasLength = Object.keys(schemas).length;

  logTitle(schemasLength);

  for (let schema in schemas) {
    console.log(`  • ${chalk.cyan(schema)}`);
    const schemaModule = schemas[schema];

    if (schemaModule.typeDefs) typeDefs.push(schemaModule.typeDefs);
    if (schemaModule.resolvers) resolvers.push(schemaModule.resolvers);
  }

  return makeExecutableSchema({ typeDefs, resolvers });
}

module.exports = {
  schema: combineSchemas(rootSchema, Schemas),
};
