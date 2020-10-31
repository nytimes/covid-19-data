const { makeExecutableSchema } = require('apollo-server');
const gql = require('graphql-tag');
const chalk = require('chalk');

const Schemas = require('./app');
const ScalarTypes = require('./scalarTypes');
const { logTitle, logSchemaModuleListItem, applyLoggingToQueryResolvers } = require('./logging');

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

function combineSchemas({ schemas, options = {} }) {
  logTitle(Object.keys(Schemas).length);
  const schemasFlat = schemas.map((schema) => Object.entries(schema)).flat();

  let index = 0;
  const combined = schemasFlat.reduce(
    (output, [name, schema]) => {
      if (schema.appModule) logSchemaModuleListItem(index, schemasFlat.length, name, schema);
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

  return makeExecutableSchema(combined);
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
