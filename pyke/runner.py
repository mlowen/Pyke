import sys
import os

from . import BuildRunner
from . import buildfile

def run():
	args = sys.argv[1:]
	argc = len(args)
	
	cwd = os.getcwd()
	default_build_file = buildfile.get_default_filename()
	pyke_path = os.path.join(cwd, '.pyke')
	build_file_path = None
	target = None
	
	# This needs to be rewritten to have proper argument parsing
	if argc == 2: # We have both the build script and target specified
		if os.path.isabs(args[0]):
			build_file_path = args[0]
		else:
			build_file_path = os.path.join(cwd, args[0])
		
		target = args[1]
	elif argc == 1:
		target = args[0]
	
	if build_file_path == None and default_build_file in os.listdir(cwd):
		build_file_path = os.path.join(cwd, default_build_file) 
	
	if not build_file_path == None:
		build_file = buildfile.load(build_file_path)
	
	if not os.path.exists(pyke_path):
		os.mkdir(pyke_path)
	
	runner = BuildRunner(build_file, pyke_path)
	
	ret = runner.run(target)
	
	runner.write_pyke_file()
	
	if ret:
		sys.exit(ret)

if __name__ == '__main__':
	run()