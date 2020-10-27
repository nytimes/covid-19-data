const glob = require('glob');
const path = require('path');
const chalk = require('chalk');

// ---

const ENABLE_LOGGING = 0;

const log = ENABLE_LOGGING ? console.log : () => null;

const logTitle = (num) =>
  log(
    chalk.bold.yellow(
      `\nImporting ${chalk.bold.gray('(' + num + ')')} app module${num === 1 ? '' : 's'}...`
    )
  );

const logListItem = (index, length, name, path) =>
  log(
    `  ${index === length - 1 ? '└' : '├'}─ ${chalk.yellow(name)} ` + chalk.dim.gray(`▸ ${path}`)
  );

// ---

function getAppModules() {
  const appModules = {};

  try {
    const files = glob.sync('**/*.module.js', { cwd: 'src/graphql/app' });

    logTitle(files.length);

    files.forEach((file, index) => {
      const moduleName = path.dirname(file);
      const modulePath = __dirname + '/' + file;

      logListItem(index, files.length, moduleName, modulePath);
      appModules[moduleName] = {
        appModule: true,
        ...require(__dirname + '/' + file),
      };
    });
  } catch (error) {
    console.error(error);
  }

  return appModules;
}

module.exports = getAppModules();
