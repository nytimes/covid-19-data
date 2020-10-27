const glob = require('glob');
const path = require('path');
const chalk = require('chalk');

const logTitle = (num) =>
  console.log(
    chalk.bold.yellow(
      `\nImporting ${chalk.bold.gray('(' + num + ')')} app module${num === 1 ? '' : 's'}...`
    )
  );

function getAppModules() {
  const appModules = {};

  try {
    const files = glob.sync('**/*.module.js', { cwd: 'src/graphql/app' });

    logTitle(files.length);

    files.forEach((file) => {
      const moduleName = path.dirname(file);
      const modulePath = __dirname + '/' + file;
      console.log(`  • ${chalk.yellow(moduleName)} from ${chalk.yellow(modulePath)}`);
      appModules[moduleName] = require(__dirname + '/' + file);
    });
  } catch (error) {
    console.error(error);
  }

  return appModules;
}

module.exports = getAppModules();
