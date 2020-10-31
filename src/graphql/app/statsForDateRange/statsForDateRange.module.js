const gql = require('graphql-tag');

module.exports = {
  typeDefs: gql`
    type StatsForDateRange {
      # location: Location
      startDate: Date
      endDate: Date
      casesTotal: Int
      deathsTotal: Int
      # dailyStats: [StatsForDate]
    }

    input StatsForDateRangeSelect {
      # location: LocationInput
      startDate: Date
      endDate: Date
    }

    type StatsForDate {
      # location: Location
      date: Date
      cases: Int
      deaths: Int
    }

    extend type Query {
      statsForDateRange(select: StatsForDateRangeSelect!): StatsForDateRange
    }
  `,
  resolvers: {
    Query: {
      statsForDateRange: (obj, args, context, info) => {
        console.log('[rkd] statsForDateRange()');
        return {};
      },
    },
    StatsForDateRange: {
      startDate: (obj, args, context, info) => new Date(),
    },
  },
};
