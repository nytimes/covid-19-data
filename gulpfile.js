const { src, dest, parallel, watch } = require("gulp");
const browserSync = require("browser-sync").create();
const sass = require("gulp-sass");
const postcss = require("gulp-postcss");
const autoprefixer = require("autoprefixer");
const cssnano = require("cssnano");
const sourcemaps = require("gulp-sourcemaps");

function scss() {
  return (
    src("./app/scss/**/*.scss")
      .pipe(sass())
      .on("error", sass.logError)
      // Use postcss with autoprefixer and compress the compiled file using cssnano
      .pipe(postcss([autoprefixer(), cssnano()]))
      // Now add/write the sourcemaps
      .pipe(sourcemaps.write())
      .pipe(dest("app/css"))
      .pipe(browserSync.stream())
  );
}

function reload(done) {
  browserSync.reload();
  done();
}

exports.css = scss;
exports.serve = function() {
  browserSync.init({
    server: {
      baseDir: "./app"
    }
  });
  watch("app/scss/**/*.scss", { ignoreInitial: false }, scss);
  watch("app/**/*.html", reload);
  watch("app/**/*.js", reload);
};
// const watch = () => watch(paths.scripts.src, gulp.series(scripts, reload));
exports.default = parallel(scss);
