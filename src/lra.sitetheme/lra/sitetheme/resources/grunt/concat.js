module.exports = {
    options: {
        banner: '<%= banner %>',
        stripBanners: false
    },
    dist: {
        src: [
            //'bower_components/jquery/dist/jquery.js',
            //'bower_components/modernizr/modernizr.js',
            //'bower_components/bootstrap/js/transition.js',
            //'bower_components/bootstrap/js/collapse.js',
            //'bower_components/bootstrap/js/dropdown.js',
            //'bower_components/holderjs/holder.js',
            //'bower_components/hideShowPassword/hideShowPassword.js',
            //'bower_components/mailcheck/src/mailcheck.js',
            //'bower_components/blazy/blazy.js',
            'js/main.js'
        ],
        dest: '<%= config.dist %>/js/<%= pkg.name %>.js'
    },
    theme: {
        src: [
            'bower_components/jquery/dist/jquery.js',
            'bower_components/modernizr/modernizr.js',
            'bower_components/bootstrap/js/transition.js',
            'bower_components/bootstrap/js/collapse.js',
            'bower_components/bootstrap/js/dropdown.js',
            'bower_components/hideShowPassword/hideShowPassword.js',
            'bower_components/mailcheck/src/mailcheck.js',
            'bower_components/blazy/blazy.js',
            'js/main.js'
        ],
        dest: '<%= config.dist %>/js/main.js'
    }
};