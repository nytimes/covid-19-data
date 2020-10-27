const gql = require('graphql-tag');

module.exports = {
  typeDefs: gql`
    extend type Query {
      rkd: String
    }
  `,
  resolvers: {
    Query: {
      rkd: () => 'RKD!',
    },
  },
};
