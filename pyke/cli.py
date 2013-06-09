import os
import sys
import argparse
import pyke

BUILD = 1
CLEAN = 2
REBUILD = 3
GENERATE_DEPENDENCIES = 4

def version():
	print('%s %s' % (pyke.__name__, pyke.__version__))
	print('Copyright (C) 2013 %s' % pyke.__author__)
	print('Available for use under the %s license.' % pyke.__license__)
	
def main():
	parser = argparse.ArgumentParser(description = pyke.__description__)
		
	# Command line arguments
	parser.add_argument('-t', '--targets', dest = 'targets', 
		metavar = 'target', nargs = '+', type = str, default = [ pyke.DEFAULT_TARGET ], 
		help = 'Targets to build, default target is \'%s\'' % pyke.DEFAULT_TARGET)
	
	parser.add_argument('-f', '--file', dest = 'build_file',
		metavar = 'file', type = str, default = pyke.DEFAULT_FILE_NAME,
		help = 'The build file to load, default file name is \'%s\'' % pyke.DEFAULT_FILE_NAME)
	
	parser.add_argument('-v', '--version', dest = 'display_version',
		action = 'store_true', help = 'Displays version information')
	
	parser.add_argument('-l', '--list', dest = 'list_targets', action = 'store_true', 
		help = 'Lists all of the available targets in the build file.')
	
	parser.add_argument('-a', '--all', dest = 'all_targets',
		action = 'store_true', help = 'Run build/clean against all targets in the build file.')
	
	parser.add_argument('-c', '--clean', dest = 'action', action = 'store_const', 
		const = CLEAN, help = 'Remove all build artifacts generated when the target is built.')

	parser.add_argument('-d', '--dependencies', dest = 'action', action = 'store_const', const = GENERATE_DEPENDENCIES,
		help = 'Generate and store the dependencies for the source files in the target.')
	
	parser.add_argument('-r', '--rebuild', dest = 'action', action = 'store_const', const = REBUILD,
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
		
		build_file = pyke.File(build_file_path)
		
		if args.list_targets:
			for t in build_file:
				print(t)
		else:
			ret = 0
			
			targets = build_file.targets() if args.all_targets else args.targets

			try:
				if args.action == CLEAN:
					for t in targets: build_file[t].clean()
				elif args.action == REBUILD:
					for t in targets: build_file[t].rebuild()
				elif args.action == GENERATE_DEPENDENCIES:
					for t in targets: build_file[t].generate_dependencies()
				else:
					built = []

					for t in targets: 
						built = build_file[t].build(built = built)
			except pyke.PykeException as e:
				print(e)
				ret = 1
			except Exception as e:
				print('An error occurred while building your project, see above for details.')
				print(e)
				ret = 1
			
			build_file.meta.write()
			sys.exit(ret)
