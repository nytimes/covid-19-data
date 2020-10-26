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

const DateType = new GraphQLScalarType({
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
});

const typeDefs = gql`
  scalar Date

  # Location Types
  type State implements Location {
    id: ID!
    name: String!
    population: Int
    counties: [County]
  }

  type County implements Location {
    id: ID!
    name: String!
    population: Int
    state: State!
  }

  interface Location {
    id: ID!
    name: String!
    population: Int
  }

  input LocationInput {
    id: ID
    name: String
    state: String
  }

  # Stats Types
  type StatsForDateRange {
    location: Location
    startDate: Date
    endDate: Date
    casesTotal: Int
    deathsTotal: Int
    dailyStats: [StatsForDate]
  }

  input StatsForDateRangeSelect {
    location: LocationInput
    startDate: Date
    endDate: Date
  }

  type StatsForDate {
    location: Location
    date: Date
    cases: Int
    deaths: Int
  }

  # Query
  type Query {
    # States
    states: [State]
    state: State

    # Counties
    counties: [County]
    county: County

    # Stats
    statsForDateRange(select: StatsForDateRangeSelect!): StatsForDateRange
  }
`;

const resolvers = {
  Date: DateType,
  Query: {
    states: () => states,
    state: () => states,
    statsForDateRange: (obj, args, context, info) => {
      console.log('[rkd] (obj, args, context, info):', (obj, args, context, info));

      return [null];
    },
  },
  Location: {
    __resolveType(location, context, info) {
      if (location.counties) {
        return 'State';
      }

      if (location.state) {
        return 'County';
      }

      return null;
    },
  },
};

// The ApolloServer constructor requires two parameters: your schema
// definition and your set of resolvers.
const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
  console.log(`🚀  Server ready at ${url}`);
});
