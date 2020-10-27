const gql = require('graphql-tag');

module.exports = {
  typeDefs: gql`
    extend type Query {
      rkd: String
      start: Date
    }
  `,
  resolvers: {
    Query: {
      rkd: () => 'RKD!',
      start: () => new Date(),
    },
  },
};
