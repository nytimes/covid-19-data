const gql = require('graphql-tag');

module.exports = {
  typeDefs: gql`
    interface Location {
      id: ID!
      name: String!
    }

    input LocationInput {
      id: ID
      name: String
    }
  `,
  resolvers: {
    Location: {
      __resolveType: (obj) => {
        return 'State';
      },
    },
  },
};
