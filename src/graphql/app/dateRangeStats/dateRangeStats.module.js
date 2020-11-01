const gql = require('graphql-tag');
const DateRangeStats = require('./controller');

module.exports = {
  typeDefs: gql`
    type DateRangeStats {
      # location: Location
      startDate: Date
      endDate: Date
      casesTotal: Int
      deathsTotal: Int
      # dailyStats: [DateStats]
    }

    input DateRangeStatsSelect {
      # location: LocationInput
      startDate: Date
      endDate: Date
    }

    type DateStats {
      # location: Location
      date: Date
      cases: Int
      deaths: Int
    }

    extend type Query {
      dateRangeStats(select: DateRangeStatsSelect!): DateRangeStats
    }
  `,
  resolvers: {
    Query: {
      dateRangeStats: (obj, args, context, info) => DateRangeStats.query(args),
    },
    DateRangeStats: {},
  },
};
