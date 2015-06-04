module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            options: {
                banner: '/*!\n' +
                    ' * <%= pkg.name %> v<%= pkg.version %>\n' +
                    ' * <%= pkg.description %>\n' +
                    ' * \n' +
                    ' * Last Modified: <%= grunt.template.today("mm-dd-yyyy") %>\n' +
                    ' * \n' +
                    ' * Created By: <%= pkg.author %>\n' +
                    ' */\n'
            },
            main: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= pkg.apps.main.js %>',
                        src: ['*.js'],
                        dest: '<%= pkg.apps.main.js %>/min/',
                        ext: '.min.js',
                        extDot: 'last'
                    }
                ]
            },
            papers: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= pkg.apps.papers.js %>',
                        src: ['*.js'],
                        dest: '<%= pkg.apps.papers.js %>/min/',
                        ext: '.min.js',
                        extDot: 'last'
                    }
                ]
            },
            account: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= pkg.apps.account.js %>',
                        src: ['*.js'],
                        dest: '<%= pkg.apps.account.js %>/min/',
                        ext: '.min.js',
                        extDot: 'last'
                    }
                ]
            },
            classes: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= pkg.apps.classes.js %>',
                        src: ['*.js'],
                        dest: '<%= pkg.apps.classes.js %>/min/',
                        ext: '.min.js',
                        extDot: 'last'
                    }
                ]
            }
        },
        coffee: {
            main: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= pkg.apps.main.coffee %>',
                        src: ['*.coffee'],
                        dest: '<%= pkg.apps.main.js %>/',
                        ext: '.js',
                        extDot: 'last'
                    }
                ]
            },
            papers: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= pkg.apps.papers.coffee %>',
                        src: ['*.coffee'],
                        dest: '<%= pkg.apps.papers.js %>/',
                        ext: '.js',
                        extDot: 'last'
                    }
                ]
            },
            account: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= pkg.apps.account.coffee %>',
                        src: ['*.coffee'],
                        dest: '<%= pkg.apps.account.js %>/',
                        ext: '.js',
                        extDot: 'last'
                    }
                ]
            },
            classes: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= pkg.apps.classes.coffee %>',
                        src: ['*.coffee'],
                        dest: '<%= pkg.apps.classes.js %>/',
                        ext: '.js',
                        extDot: 'last'
                    }
                ]
            }
        },
        compass: {
            main: {
                options: {
                    sassDir: '<%= pkg.apps.main.sass %>',
                    cssDir: '<%= pkg.apps.main.css %>',
                    noLineComments: true,
                    outputStyle: 'compressed'
                }
            },
            papers: {
                options: {
                    sassDir: '<%= pkg.apps.papers.sass %>',
                    cssDir: '<%= pkg.apps.papers.css %>',
                    noLineComments: true,
                    outputStyle: 'compressed'
                }
            },
            account: {
                options: {
                    sassDir: '<%= pkg.apps.account.sass %>',
                    cssDir: '<%= pkg.apps.account.css %>',
                    noLineComments: true,
                    outputStyle: 'compressed'
                }
            },
            classes: {
                options: {
                    sassDir: '<%= pkg.apps.classes.sass %>',
                    cssDir: '<%= pkg.apps.classes.css %>',
                    noLineComments: true,
                    outputStyle: 'compressed'
                }
            }
        },
        watch: {
            options: {
                cwd: 'Writerr/'
            },
            main_coffee: {
                files: ['main/coffee/*.coffee'],
                tasks: ['coffee:main', 'uglify:main']
            },
            papers_coffee: {
                files: ['papers/coffee/*.coffee'],
                tasks: ['coffee:papers', 'uglify:papers']
            },
            account_coffee: {
                files: ['account/coffee/*.coffee'],
                tasks: ['coffee:account', 'uglify:account']
            },
            classes_coffee: {
                files: ['classes/coffee/*.coffee'],
                tasks: ['coffee:classes', 'uglify:classes']
            },
            main_sass: {
                files: ['main/design/*.scss'],
                tasks: ['compass:main']
            },
            papers_sass: {
                files: ['papers/design/*.scss'],
                tasks: ['compass:papers']
            },
            account_sass: {
                files: ['account/design/*.scss'],
                tasks: ['compass:account']
            },
            classes_sass: {
                files: ['classes/design/*.scss'],
                tasks: ['compass:classes']
            }
        },

        clean: {
            main: ['<%= pkg.apps.main.js %>/*.js', '<%= pkg.apps.main.sass %>', '<%= pkg.apps.main.coffee %>'],
            papers: ['<%= pkg.apps.papers.js %>/*.js', '<%= pkg.apps.papers.sass %>', '<%= pkg.apps.papers.coffee %>'],
            account: ['<%= pkg.apps.account.js %>/*.js', '<%= pkg.apps.account.sass %>', '<%= pkg.apps.account.coffee %>'],
            classes: ['<%= pkg.apps.classes.js %>/*.js', '<%= pkg.apps.classes.sass %>', '<%= pkg.apps.classes.coffee %>']
        }
    });


    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-coffee');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-clean');

  // Default task(s).
    grunt.registerTask('default', ['coffee', 'uglify', 'compass']);

};