const gql = require('graphql-tag');

module.exports = {
  typeDefs: gql`
    extend type Query {
      rkd2: String
      start2: Date
      start3: Date
    }
  `,
  resolvers: {
    Query: {
      rkd2: () => 'RKD!',
      start2: () => new Date(),
      start3: () => new Date(),
    },
  },
};
