const { ApolloServer } = require('apollo-server');
const chalk = require('chalk');

const line = '-------------------------------------------------------';
console.log(chalk.bold.green(`\n${line}\nLaunching server\n${line}`));

const { makeAppSchema } = require('./schema');

// const typeDefs = gql`
//   scalar Date

//   # Location Types
//   type State implements Location {
//     id: ID!
//     name: String!
//     population: Int
//     counties: [County]
//   }

//   type County implements Location {
//     id: ID!
//     name: String!
//     population: Int
//     state: State!
//   }

//   interface Location {
//     id: ID!
//     name: String!
//     population: Int
//   }

//   input LocationInput {
//     id: ID
//     name: String
//     state: String
//   }

//   # Stats Types
//   type StatsForDateRange {
//     location: Location
//     startDate: Date
//     endDate: Date
//     casesTotal: Int
//     deathsTotal: Int
//     dailyStats: [StatsForDate]
//   }

//   input StatsForDateRangeSelect {
//     location: LocationInput
//     startDate: Date
//     endDate: Date
//   }

//   type StatsForDate {
//     location: Location
//     date: Date
//     cases: Int
//     deaths: Int
//   }

//   # Query
//   type Query {
//     # States
//     states: [State]
//     state: State

//     # Counties
//     counties: [County]
//     county: County

//     # Stats
//     statsForDateRange(select: StatsForDateRangeSelect!): StatsForDateRange
//   }
// `;

// const resolvers = {
//   Date: DateType,
//   Query: {
//     states: () => states,
//     state: () => states,
//     statsForDateRange: (obj, args, context, info) => {
//       console.log('[rkd] (obj, args, context, info):', (obj, args, context, info));

//       return [null];
//     },
//   },
//   Location: {
//     __resolveType(location, context, info) {
//       if (location.counties) {
//         return 'State';
//       }

//       if (location.state) {
//         return 'County';
//       }

//       return null;
//     },
//   },
// };

const server = new ApolloServer({
  schema: makeAppSchema({ enableLogging: true }),
});

server.listen().then(({ url }) => {
  console.log(`\n🚀  Server ready at ${chalk.blue.underline(url)}`);
});
