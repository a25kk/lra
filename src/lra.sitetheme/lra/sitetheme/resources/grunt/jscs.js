// task: jscs
module.exports = {
  options: {
    jshintrc: 'js/.jscsrc'
  },
  grunt: {
    src: 'Gruntfile.js'
  },
  src: {
    src: ['js/*.js']
  }
};