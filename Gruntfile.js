module.exports = function(grunt) {

  grunt.initConfig({
     watch: {

            coffee : {
                files: ['scrum/src/coffee/*.coffee', 'scrum/src/coffee/*/*.coffee'],
                tasks: ['coffee:compile', 'concat'],
            },

            js : {
                files: 
                [
                'scrum/src/js/*.js',
                'scrum/src/coffee/*.js',
                ],
                tasks: ['concat']
            },


      },

      coffee: {
            compile: {
              options: {
                bare: true
              },
                files: {
                      'scrum/static/js/_coffee.js': [
                      'scrum/src/coffee/main.coffee', 
                      'scrum/src/coffee/*.coffee', 
                      'scrum/src/coffee/*/*.coffee'
                    ]
                }
            }
        },

        concat: {
            dist: {
                src: [
                     'scrum/static/js/_coffee.js',
                     'scrum/src/js/js.js',
                     ],
                dest: 'scrum/static/js/prod.js'

            }
        },
  });

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['watch:coffee', 'watch:js', 'concat']);

};