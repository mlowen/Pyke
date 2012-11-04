import os
import sys
import argparse

from pyke import runner
from pyke import buildfile

# Meta Information
__version__ = '0.2.4-alpha'
__name__ = 'Pyke'
__description__ = 'Pyke is a build system for the gcc c++ compiler.'
__author__ = 'Mike Lowen'
__author_email__ = 'mike@mlowen.com'
__homepage__ = 'http://mlowen.com'
__license__ = 'MIT'

def version():
	print('%s %s' % (__name__, __version__))
	print('Copyright (C) 2012 %s' % __author__)
	print('Available for use under the %s license.' % __license__)
	
def main():
	parser = argparse.ArgumentParser(description = 'A C++ build tool.')
	
	# Command line arguments
	parser.add_argument('-t', '--target', dest = 'targets', 
		metavar = 'target', nargs = '+', type = str, default = target.get_default_target(), 
		help = 'Targets to build, default target is \'%s\'' % target.get_default_target())
	
	parser.add_argument('-f', '--file', dest = 'build_file',
		metavar = 'file', type = str, default = buildfile.get_default_filename(),
		help = 'The build file to load, default file name is \'%s\'' % buildfile.get_default_filename())
	
	parser.add_argument('-v', '--version', dest = 'display_version',
		action = 'store_true', help = 'Displays version information')
	
	parser.add_argument('-l', '--list', dest = 'list_targets',
		action = 'store_true', help = 'Lists all of the available targets in the build file.')
	
	parser.add_argument('-c', '--clean', dest = 'clean_target',
		action = 'store_true', help = 'Remove all build artifacts generated when the target is built.')
	
	parser.add_argument('-a', '--all', dest = 'all_targets',
		action = 'store_true', help = 'Run build/clean against all targets in the build file.')
	
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
		
		build_file = buildfile.load(build_file_path)
		
		if args.list_targets:
			for t in build_file.get_all_targets():
				print(t)
		else:
			base_path = os.path.dirname(build_file_path) 	
			
			os.chdir(base_path)
			
			build_runner = runner.BuildRunner(build_file, base_path)
			ret = None
			
			try:
				if args.clean_target:
					if args.all_targets:
						build_runner.clean_all()
					else:
						build_runner.clean(args.targets)
				else:
					if args.all_targets:
						build_runner.build_all()
					else:
						build_runner.build(args.targets)
			except Exception as e:
				print('An error occurred while building your project, see above for details.')
				print(e)
				ret = 1
			
			build_runner.write_pyke_file()
		
			if not ret == None:
				sys.exit(ret)

if __name__ == '__main__':
	main()