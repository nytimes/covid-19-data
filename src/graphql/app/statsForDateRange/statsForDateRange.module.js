const gql = require('graphql-tag');

module.exports = {
  typeDefs: gql`
    extend type Query {
      rkd: String
      start: Date
      blah1: String
      blah2: String
      blah3: String
      blah0: String
      blah7: String
      blah8: String
      blah9: String
    }
  `,
  resolvers: {
    Query: {
      rkd: () => 'RKD!',
      start: () => new Date(),
    },
    Mutation: {
      blah7: () => null,
      blah8: () => null,
      blah9: () => null,
      blah0: () => null,
      blah1: () => null,
      blah2: () => null,
      blah3: () => null,
    },
  },
};
