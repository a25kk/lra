import gulp from 'gulp';
import gulpLoadPlugins from 'gulp-load-plugins';
import browserSync from 'browser-sync';
import del from 'del';
import args from 'yargs';
import {stream as wiredep} from 'wiredep';

const $ = gulpLoadPlugins();
const reload = browserSync.reload;

var cp = require('child_process');
var pkg = require('./package.json');

var messages = {
    jekyllBuild: '<span style="color: grey">Running:</span> $ jekyll build'
};

var basePaths = {
    app: 'app',
    dev: '_site',
    dist: 'dist',
    diazoPrefix: '/++theme++pkg.name.sitetheme',
    bower: 'bower_components/'
};

var sourcesJS = {
    base: [
        basePaths.bower + 'bootstrap-without-jquery/bootstrap3/bootstrap-without-jquery.js',
        basePaths.bower + 'lazysizes/lazysizes.js',
        basePaths.bower + 'flickity/dist/flickity.pkgd.js'
    ],
    all: [
        basePaths.bower + 'jquery/dist/jquery.js',
        basePaths.bower + 'modernizr/modernizr.js',
        basePaths.bower + 'bootstrap-without-jquery/bootstrap3/bootstrap-without-jquery.js',
        basePaths.bower + 'mailcheck/src/mailcheck.js',
        basePaths.bower + 'JVFloat/jvfloat.js',
        basePaths.bower + 'hideShowPassword/hideShowPassword.js',
        basePaths.bower + 'lazysizes/lazysizes.js',
        basePaths.bower + 'flickity/dist/flickity.pkgd.js'

    ]
};

var isProduction = args.env === 'dist';

/**
 * Build the Jekyll Site
 */
gulp.task('jekyll-build', function (done) {
    browserSync.notify(messages.jekyllBuild);
    return cp.spawn('jekyll', ['build'], {stdio: 'inherit'})
        .on('close', done);
});

gulp.task('browser-sync', function () {
    browserSync({
        server: {
            baseDir: "./"
        }
    });
});

gulp.task('bs-reload', function () {
    browserSync.reload();
});

gulp.task('styles', () = > {
    return gulp.src(basePaths.app + '/sass/main.scss')
        .pipe($.plumber())
        .pipe($.sourcemaps.init())
        .pipe($.sass.sync({
            outputStyle: 'expanded',
            precision: 10,
            includePaths: [basePaths.bower]
        }).on('error', $.sass.logError))
        .pipe($.autoprefixer({browsers: ['last 1 version']}))
        .pipe(gulp.dest(basePaths.dist + '/styles/'))
        .pipe($.minifyCss())
        .pipe($.rename({
            basename: pkg.name,
            suffix: '.min'
        }))
        .pipe($.sourcemaps.write())
        .pipe(gulp.dest(basePaths.dist + '/styles/'))
        .pipe(reload({stream: true}));
})
;

gulp.task('scripts', () = > {
    return gulp.src(isProduction ? sourcesJS.all : sourcesJS.base)
        .pipe($.plumber({
            errorHandler: function (error) {
                console.log(error.message);
                this.emit('end');
            }
        }))
        .pipe($.jshint())
        .pipe($.jshint.reporter('default'))
        .pipe($.concat(pkg.name + '.js'))
        .pipe(gulp.dest(basePaths.dist + 'scripts/'))
        .pipe($.rename({suffix: '.min'}))
        .pipe($.uglify())
        .pipe(gulp.dest(basePaths.dist + '/scripts/'))
        .pipe(browserSync.reload({stream: true}));
})
;

gulp.task('images', () = > {
    return gulp.src(basePaths.app + 'assets/img/**/*')
        .pipe($.if($.if.isFile, $.cache($.imagemin({
            progressive: true,
            interlaced: true,
            // don't remove IDs from SVGs, they are often used
            // as hooks for embedding and styling
            svgoPlugins: [{cleanupIDs: false}]
        }))
            .on('error', function (err) {
                console.log(err);
                this.end();
            })))
        .pipe(gulp.dest(basePaths.dist + 'assets/img'));
})
;

gulp.task('fonts', () = > {
    return gulp.src(require('main-bower-files')({
        filter: '**/*.{eot,svg,ttf,woff,woff2}'
    }).concat(basePaths.app + 'assets/fonts/**/*'))
        .pipe(gulp.dest('.tmp/fonts'))
        .pipe(gulp.dest(basePaths.dist + 'assets/fonts'));
})
;

gulp.task('html', () = > {
    return gulp.src(basePaths.dev + '{,*/}*.html')
        .pipe($.minifyHtml())
        .pipe(gulp.dest(basePaths.dist));
})
;

gulp.task('cb', () = > {
    return gulp.src(basePaths.dist + 'styles/*.min.css')
        .pipe($.rev())
        .pipe(gulp.dest(basePaths.dist + '/styles'))
        .pipe($.rev.manifest())
        .pipe($.revDel({dest: basePaths.dist + '/styles'}))
        .pipe(gulp.dest(basePaths.dist + '/styles'))
}
)
;

gulp.task('revreplace', () = > {
    var manifest = gulp.src(basePaths.dist + '/styles/rev-manifest.json');
    return gulp.src(basePaths.dev + '/{,*/}*.html')
        .pipe(revReplace({manifest: manifest}))
        .pipe(gulp.dest(basePaths.dev));
})
;

gulp.task('replace', () = > {
    return gulp.src(basePaths.dev + '/{,*/}*.html')
        .pipe(replace({
            patterns: [
                {
                    match: '../../assets/',
                    replacement: '../assets/'
                }
            ],
            usePrefix: false,
            preserveOrder: true
        }))
        .pipe(gulp.dest(basePaths.dev))
});

gulp.task('default', ['browser-sync'], function () {
    gulp.watch(basePaths.app + "sass/**/*.scss", ['styles']);
    gulp.watch(basePaths.app + "scripts/**/*.js", ['scripts']);
    gulp.watch(basePaths.app + "*.html", ['bs-reload']);
});
