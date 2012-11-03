# Pyke
Pyke is a python build tool which is designed to be simple to use and configure, which also allows you to use the full power of python in your build scripts.

## Installation

To install pyke you need to have a package that supplies easy\_install installed (personally I use [distribute](http://pypi.python.org/pypi/distribute/)).  Once you have easy\_install  and a copy of the source code you can install pyke by running the following command from the source:

`python setup.py install`

## Usage

`pyke [-h] [-t, --target t] [-f, --file f]`

### Optional Arguments:
* `-h, --help` Show the help message and exit
* `-t, --target t` Target to build, default target is 'default'
* `-f, --file f` The build file to load, default file name is 'build.pyke'

## Pyke File

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