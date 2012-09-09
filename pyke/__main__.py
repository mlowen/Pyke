import sys
import os

from . import main

if __name__ == '__main__':
	args = sys.argv[1:]
	argc = len(args)
	
	cwd = os.getcwd()
	default_build_file = 'build.pyke'
	build_file = None
	target = None
	
	if argc == 2: # We have both the build script and target specified
		if os.path.abs(build_file):
			build_file = args[0]
		else:
			build_file = os.path.join(cwd, args[0])
		
		target = args [1]
	elif argc == 1:
		target = args[0]
	
	if build_file == None and default_build_file in os.listdir(cwd):
		build_file = os.path.join(cwd, default_build_file) 
	
	ret = main(build_file, target)
	
	if ret:
		sys.ext(ret)