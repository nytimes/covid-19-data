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

    console.log(`\n${operationColor(operationType)} ${chalk.cyanBright(operationName)}`);
    console.log(`${operationColor('args')}`);
    console.log(chalk.gray(JSON.stringify(args, null, 2)));

    try {
      return resolver(root, args, ctx, info);
    } catch (err) {
      console.error(chalk.white.bold.bgRed('  E R R O R  '));
      const stackSplit = err.stack.split('\n');
      const firstLine = stackSplit.shift();
      console.error(chalk.red.bold(firstLine));

      const atRegex = /^\s+at\s{1}/i;
      const pathInParensRegex = /\(([^\)]+)\)/i;
      const pathRegex = /\(?\/[^\)]+:\d+$/i;

      console.error(
        stackSplit
          .map((stackLine) => {
            return stackLine
              .replace(atRegex, ($1) => chalk.dim.red($1) + chalk.reset())
              .replace(pathInParensRegex, ($1) => chalk.dim.red($1) + chalk.reset())
              .replace(pathRegex, ($1) => chalk.dim.red($1) + chalk.reset());
          })
          .join('\n')
      );
      return err;
    }
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
