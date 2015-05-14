module.exports = function(grunt) {

    "use strict";

    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        uglify: {
            dist: {
                files: {
                    "uploader/static/uploader/js/uploader.min.js": "uploader/static/uploader/js/uploader.js"
                }
            }
        },
        concat: {
            dist: {
                options: {
                    separator: "\n\n"
                },
                src: [
                    "uploader/static/uploader/js/jquery.ui.widget.js",
                    "uploader/static/uploader/js/jquery.iframe-transport.js",
                    'uploader/static/uploader/js/load-image.js',
                    'uploader/static/uploader/js/load-image-ios.js',
                    'uploader/static/uploader/js/load-image-orientation.js',
                    'uploader/static/uploader/js/load-image-meta.js',
                    'uploader/static/uploader/js/load-image-exif.js',
                    'uploader/static/uploader/js/load-image-exif-map.js',
                    "uploader/static/uploader/js/canvas-to-blob.js",
                    "uploader/static/uploader/js/tmpl.js",
                    "uploader/static/uploader/js/jquery.fileupload.js",
                    "uploader/static/uploader/js/jquery.fileupload-ui.js",
                    "uploader/static/uploader/js/jquery.fileupload-process.js",
                    "uploader/static/uploader/js/jquery.fileupload-audio.js",
                    "uploader/static/uploader/js/jquery.fileupload-image.js",
                    "uploader/static/uploader/js/jquery.fileupload-video.js",
                    "uploader/static/uploader/js/jquery.fileupload-validate.js",
                    "uploader/static/uploader/js/csrf.js",
                ],
                dest: "uploader/static/uploader/js/uploader.js"
            }
        }
    });

    // Load grunt tasks from NPM packages
    grunt.loadNpmTasks("grunt-contrib-concat");
    grunt.loadNpmTasks("grunt-contrib-uglify");

    // Register grunt tasks
    grunt.registerTask("default", ["concat", "uglify"]);

};
