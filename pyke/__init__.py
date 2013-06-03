import os
import sys
import argparse

from pyke import defaults
from pyke import runners
from pyke import buildfile

# Meta Information
__version__ = '0.5.0-beta'
__name__ = 'Pyke'
__description__ = 'Build system for the GCC C++ compiler.'
__author__ = 'Mike Lowen'
__author_email__ = 'mike@mlowen.com'
__homepage__ = 'http://mlowen.com'
__license__ = 'MIT'

class TargetWrapper:
	def __init__(self, fn):
		self.fn = fn

def target(fn):
	return TargetWrapper(fn)

def version():
	print('%s %s' % (__name__, __version__))
	print('Copyright (C) 2013 %s' % __author__)
	print('Available for use under the %s license.' % __license__)
	
def main():
	parser = argparse.ArgumentParser(description = __description__)
		
	# Command line arguments
	parser.add_argument('-t', '--target', dest = 'targets', 
		metavar = 'target', nargs = '+', type = str, default = defaults.get_target(), 
		help = 'Targets to build, default target is \'%s\'' % defaults.get_target())
	
	parser.add_argument('-f', '--file', dest = 'build_file',
		metavar = 'file', type = str, default = defaults.get_filename(),
		help = 'The build file to load, default file name is \'%s\'' % defaults.get_filename())
	
	parser.add_argument('-v', '--version', dest = 'display_version',
		action = 'store_true', help = 'Displays version information')
	
	parser.add_argument('-l', '--list', dest = 'list_targets', action = 'store_true', 
		help = 'Lists all of the available targets in the build file.')
	
	parser.add_argument('-c', '--clean', dest = 'action', action = 'store_const', 
		const = 'clean', help = 'Remove all build artifacts generated when the target is built.')
	
	parser.add_argument('-a', '--all', dest = 'all_targets',
		action = 'store_true', help = 'Run build/clean against all targets in the build file.')
	
	parser.add_argument('-d', '--dependencies', dest = 'action', action = 'store_const', const = 'dependencies',
		help = 'Generate and store the dependencies for the source files in the target.')
	
	parser.add_argument('-r', '--rebuild', dest = 'action', action = 'store_const', const = 'rebuild',
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
		
		build_file = buildfile.File(build_file_path)
		
		if args.list_targets:
			for t in build_file:
				print(t)

		if args.list_targets:
			for t in build_file.get_all_targets():
				print(t)
		else:
			base_path = os.path.dirname(build_file_path)
			
			os.chdir(base_path)
			
			runner = runners.factory(args.action, build_file, base_path)
			ret = 0
			
			#try:
			if args.all_targets:
				runner.run_all()
			else:
				runner.run(args.targets)
			#except runners.RunnerException as e:
			#	print(e)
			#	ret = 1
			#except Exception as e:
			#	print('An error occurred while building your project, see above for details.')
			#	print(e)
			#	ret = 1
			
			runner.write_meta_data()
			sys.exit(ret)

if __name__ == '__main__':
	main()