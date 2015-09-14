module.exports = {
    options: {
        banner: '<%= banner %>'
    },
    dist: {
      files: {
        '<%= config.dist %>/js/<%= pkg.name %>.min.js': ['<%= config.dist %>/js/<%= pkg.name %>.js']
      }
    }
};