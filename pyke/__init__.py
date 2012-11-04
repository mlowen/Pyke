import os
import argparse

from pyke import runner
from pyke import buildfile

# Meta Information
__version__ = '0.2.2-alpha'
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
	
	parser.add_argument('-t', '--target', dest = 'target', 
		metavar = 'target', type = str, default = target.get_default_target(), 
		help = 'Target to build, default target is \'%s\'' % target.get_default_target())
	
	parser.add_argument('-f', '--file', dest = 'build_file',
		metavar = 'file', type = str, default = buildfile.get_default_filename(),
		help = 'The build file to load, default file name is \'%s\'' % buildfile.get_default_filename())
	
	parser.add_argument('-v', '--version', dest = 'display_version',
		action = 'store_true', help = 'Displays version information')
		
	args = parser.parse_args()
	
	if args.display_version:
		version()
	else:
		build_file_path = None
		
		if os.path.isabs(args.build_file):
			build_file_path = args.build_file
		else:
			build_file_path = os.path.join(os.getcwd(), args.build_file)
		
		base_path = os.path.dirname(build_file_path) 	
		
		os.chdir(base_path)
		
		build_runner = runner.BuildRunner(buildfile.load(build_file_path), base_path)
		ret = None
		
		try:
			build_runner.build(args.target)
		except Exception as e:
			print('An error occurred while building your project, see above for details.')
			print(e)
			ret = 1
		
		build_runner.write_pyke_file()
		
		if not ret == None:
			sys.exit(ret)

if __name__ == '__main__':
	main()