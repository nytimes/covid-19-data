const chalk = require('chalk');

// --- Import/Startup Logging ---
const logTitle = (num) =>
  console.log(
    chalk.bold.yellow(
      `\nCombining ${chalk.bold.gray('(' + num + ')')} app module${num === 1 ? '' : 's'}...`
    )
  );

const logSchemaModuleListItem = (index, length, name, schema) =>
  console.log(
    `  ${index === length - 1 ? '└' : '├'}─ ${chalk.yellow(name)} `.padEnd(42) +
      chalk.dim.gray('| ') +
      chalk.cyan('•'.repeat(Object.keys(schema.resolvers?.Query || {}).length)) +
      chalk.magenta('•'.repeat(Object.keys(schema.resolvers?.Mutation || {}).length))
  );

// --- Query Resolver logging ---
function applyLogging(resolver) {
  return async (root, args, ctx, info) => {
    const operationType = info.operation.operation;
    const operationColor = operationType === 'query' ? chalk.blue : chalk.magenta;
    const operationName = info.operation.name.value;

    console.log(`\n${operationColor(operationType)} ${chalk.cyan(operationName)}`);
    console.log(`${operationColor('args')}`);
    console.log(chalk.gray(JSON.stringify(args, null, 2)));

    return resolver(root, args, ctx, info);
  };
}

function applyLoggingToQueryResolvers(resolvers) {
  if (!resolvers.Query) {
    return resolvers;
  }

  return {
    ...resolvers,
    Query: Object.fromEntries(
      Object.entries(resolvers.Query).map(([name, resolverFn]) => {
        return [name, applyLogging(resolverFn)];
      })
    ),
  };
}

// --- Exports ---

module.exports = {
  logTitle,
  logSchemaModuleListItem,
  applyLogging,
  applyLoggingToQueryResolvers,
};
