# Pyke
Pyke is a python build tool which is designed to be simple to use and configure, which also allows you to use the full power of python in your build scripts.

## Installation

To install pyke you need to have a package that supplies easy\_install installed (personally I use [distribute](http://pypi.python.org/pypi/distribute/)).  Once you have easy\_install  and a copy of the source code you can install pyke by running the following command from the source:

`python setup.py install`

## Usage

`pyke [-h] [-t target [target ...]] [-f file] [-v] [-l] [-c]`

### Optional Arguments:
* `-h, --help` show this help message and exit
* `-t target [target ...], --target target [target ...]` Targets to build, default target is 'default'
* `-f file, --file file` The build file to load, default file name is 'build.pyke'
* `-v, --version` Displays version information.
* `-l, --list` Lists all of the available targets in the build file.
* `-c, --clean` Remove all build artifacts generated when the target is built.

## Pyke File
A pyke build file for all intents and purposes is a python script, anything you can do in a python script can be done in a pyke script.  A build (including pre & post build methods) are run from the directory that the build file is located in which will be referred to as the base path in this section.

### Targets

A target in Pyke is a python method which returns a dictionary object, this object is used to decide what and how to build the target, the values that will be acted upon are as follows:

* `source_paths` This can either be a string or an array of strings, this field is used to specify the folders where your source code is located.  It is important to note that pyke recurses through the directories listed.  If no value is supplied then the base path will be used.
* `source_patterns` This can either be a string or an array of strings, this field is used for matching what files should be compiled, the [glob syntax](http://en.wikipedia.org/wiki/Glob_(programming)) is used to match the files.
* `output_path` This can only be a string, this field is used to specify the directory where the output files will be compiled to, if no value is supplied then the base path will be used.  If this directory does not exist then it will be created.
* `output_name` This can only be a string, this field is used to specify the name (sans extension) of the executable that will be generated by building the target.  If no value is specified then the name of the base path will be used.
* `compiler_flags` This can be a string or an array of strings, this field contains a list of flags to pass to the compiler.
* `linker_flags` This can be a string or an array of strings, this field contains a list of flags to pass to the linker.
* `libraries` This can be a string or an array of strings, this field contains a list of libraries (sans `-l`) to pass to the linker.  Looking at retiring this field in the future and merging it with the `linker_flags` field.

When no target name is specified in the command line Pyke will try and run a target called `default` so it is always handy to have one of your targets named `default`.

### Pre & Post Builds

The pre and post build functionality are again just python functions that are called at the appropriate times, they should take no parameters and any returns will be ignored.  The pre & post build functionality follows the naming convention of pre builds are the target name with the prefix `pre_` and post builds are the target name with the prefix `post_` so the pre-build function for the default target would be `pre_default` and the for the post-build `post_default`

### Example Build File

Below is a trivial example of a imaginary project that links to two libraries.

```python
def pre_default():
	print('Running the pre-build')

def default():
	return {
		'output_path': 'bin',
		'output_name': 'example_name',
		'source_path': [ 'src' ],
		'source_patterns': [ '*.cc', '*.cpp' ]
		'compiler_flags': [ '-WALL', '-I', '..\\libs\\include' ]
		'linker_flags': [ 'L', '..\\libs' ]
		'libraries': [ 'example-lib-a', 'example-lib-b' ]
	}

def post_default():
	print('Running the post-build')
```

## Known Issues

* Currently Pyke only uses the GNU C++ compiler, this is on the list to expand the options.
* Currently Pyke only compiles executables and not libraries.
* There is a bug in when getting all targets of a build file where if you import a function into the build file using the style `from x import y` Pyke will think that it is a valid target and when a build/clean all is run it will try and run that target.

## To Do

* An alternative JSON based build file.
* A built in 'clean' target to remove build artifacts.
* A built in 'all' to build all targets in a pyke file.
* Target Dependencies.
* Expand to other compilers.

## License
Pyke is available under the MIT license which is as follows:

Copyright (c) 2012 Michael Lowen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.