const { ApolloServer, gql } = require('apollo-server');
const { GraphQLScalarType } = require('graphql');
const { Kind } = require('graphql/language');

const states = [
  {
    title: 'The Awakening',
    author: 'Kate Chopin',
  },
  {
    title: 'City of Glass',
    author: 'Paul Auster',
  },
];

const typeDefs = gql`
  scalar Date

  # Location Types
  type State {
    id: ID!
    name: String!
    counties: [County]
    population: Int
  }

  type County {
    id: ID!
    name: String!
    state: State!
  }

  type Location {
    state: ID
    county: ID
  }

  # Stats Types
  type StatsForDateRange {
    location: Location
    startDate: Date
    endDate: Date
    casesTotal: Int
    deathsTotal: Int
  }

  type StatsForDay {
    location: Location
    date: Date
    cases: Int
    deaths: Int
  }

  # Query
  type Query {
    states: [State]
    state: State
  }
`;

const resolvers = {
  Date: new GraphQLScalarType({
    name: 'Date',
    description: 'Date custom scalar type',
    parseValue(value) {
      return new Date(value); // value from the client
    },
    serialize(value) {
      return value.getTime(); // value sent to the client
    },
    parseLiteral(ast) {
      if (ast.kind === Kind.INT) {
        return parseInt(ast.value, 10); // ast value is always in string format
      }
      return null;
    },
  }),
  Query: {
    states: () => states,
    state: () => states,
  },
};

// The ApolloServer constructor requires two parameters: your schema
// definition and your set of resolvers.
const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
  console.log(`🚀  Server ready at ${url}`);
});
