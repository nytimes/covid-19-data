const { GraphQLScalarType } = require('graphql');
const gql = require('graphql-tag');

const scalarType = new GraphQLScalarType({
  name: 'Date',
  description: 'Date custom scalar type',
  parseValue(value) {
    return new Date(value); // value from the client
  },
  serialize(value) {
    return value.toISOString(); // value sent to the client
  },
  parseLiteral(ast) {
    if (ast.kind === Kind.INT) {
      return parseInt(ast.value, 10); // ast value is always in string format
    }
    return null;
  },
});

module.exports = {
  typeDefs: gql`
    scalar Date
  `,
  resolvers: {
    Date: scalarType,
  },
};
