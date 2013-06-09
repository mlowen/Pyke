# Change Log

## vNext

* Added ability to populate the fields prebuild, postbuild & clean with methods instead of strings.
* Functions must now be decorated with `@target` to be considered as targets.
* When cleaning file dependencies are now retained.
* Updated the dependency generation so it goes more than two levels deep.
* Renamed the 'compiler' field in a build file to be 'builder'.
* Added a tidy up function to the meta file to prevent the build-up of crud.

## 0.5.0 (2013-06-01)

* Implemented target dependencies.
* Added ability to populate the fields prebuild, postbuild & clean with methods rather than just strings.
* Added 'phoney' aka no-build targets.

## 0.4.X

* Stopped the generation of \__pycache__ directories being generated in the project directory when the project is being built.
* Added the rebuild functionality.

## 0.3.X

* Added file dependency generation.

## 0.2.X

* Added the list all build targets functionality.
* Added the clean target functionality.
* Added the ability to build multiple targets.
* Added the ability to clean multiple targets.
* Added the all meta target to build all targets in a file.
* Added the ability to overwrite the convention for pre & post build functionality with custom method names.
* Added the ability to overwrite the convention for clean functionality with custom method names.
* Added the ability to build libraries.

## 0.1.X

* Build executables based on pyke file.
* Added pre & post build functionality.
* Conditional file approval based on if there has been a change to the file.