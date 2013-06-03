import os
import sys
import argparse

from . import compilers
from . import meta

from .target import TargetWrapper
from .file import File

# Meta Information
__version__ = '0.5.1-beta'
__name__ = 'Pyke'
__description__ = 'Build system for the GCC C++ compiler.'
__author__ = 'Mike Lowen'
__author_email__ = 'mike@mlowen.com'
__homepage__ = 'http://mlowen.com'
__license__ = 'MIT'

# Constants

DEFAULT_TARGET = 'default'
DEFAULT_FILE_NAME = 'build.pyke'

class PykeException(BaseException):
	def __init__(self, message):
		BaseException.__init__(message)

		self.message = message

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Actions = enum('Build', 'Clean', 'Rebuild', 'GenerateDependencies')

def target(fn):
	return TargetWrapper(fn)

def version():
	print('%s %s' % (__name__, __version__))
	print('Copyright (C) 2013 %s' % __author__)
	print('Available for use under the %s license.' % __license__)
	
def main():
	parser = argparse.ArgumentParser(description = __description__)
		
	# Command line arguments
	parser.add_argument('-t', '--targets', dest = 'targets', 
		metavar = 'target', nargs = '+', type = str, default = [ DEFAULT_TARGET ], 
		help = 'Targets to build, default target is \'%s\'' % DEFAULT_TARGET)
	
	parser.add_argument('-f', '--file', dest = 'build_file',
		metavar = 'file', type = str, default = DEFAULT_FILE_NAME,
		help = 'The build file to load, default file name is \'%s\'' % DEFAULT_FILE_NAME)
	
	parser.add_argument('-v', '--version', dest = 'display_version',
		action = 'store_true', help = 'Displays version information')
	
	parser.add_argument('-l', '--list', dest = 'list_targets', action = 'store_true', 
		help = 'Lists all of the available targets in the build file.')
	
	parser.add_argument('-a', '--all', dest = 'all_targets',
		action = 'store_true', help = 'Run build/clean against all targets in the build file.')
	
	parser.add_argument('-c', '--clean', dest = 'action', action = 'store_const', 
		const = Actions.Clean, help = 'Remove all build artifacts generated when the target is built.')

	parser.add_argument('-d', '--dependencies', dest = 'action', action = 'store_const', const = Actions.GenerateDependencies,
		help = 'Generate and store the dependencies for the source files in the target.')
	
	parser.add_argument('-r', '--rebuild', dest = 'action', action = 'store_const', const = Actions.Rebuild,
		help = 'Runs a clean followed by a build on the specified targets.')
    
	args = parser.parse_args()
	
	# Run the application
	if args.display_version:
		version()
	else:
		build_file_path = None
		
		if os.path.isabs(args.build_file):
			build_file_path = args.build_file
		else:
			build_file_path = os.path.join(os.getcwd(), args.build_file)
		
		build_file = File(build_file_path)
		
		if args.list_targets:
			for t in build_file:
				print(t)
		else:
			os.chdir(os.path.dirname(build_file_path))

			ret = 0
			
			targets = build_file.targets() if args.all_targets else args.targets

			#try:
			if args.action == Actions.Clean:
				for t in targets: build_file[t].clean()
			elif args.action == Actions.Rebuild:
				for t in targets: build_file[t].rebuild()
			elif args.action == Actions.GenerateDependencies:
				for t in targets: build_file[t].generate_dependencies()
			else:
				built = []

				for t in targets: 
					built = build_file[t].build(built = built)
			'''
			except PykeException as e:
				print(e)
				ret = 1
			except Exception as e:
				print('An error occurred while building your project, see above for details.')
				print(e)
				ret = 1
			'''
			sys.exit(ret)

if __name__ == '__main__':
	main()