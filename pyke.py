#! /bin/env python

import sys
import os

import pyke

def main():
	args = sys.argv[1:]
	argc = len(args)
	
	cwd = os.getcwd()
	default_build_file = pyke.buildfile.get_default_filename()
	build_file = None
	target = None
	
	if argc == 2: # We have both the build script and target specified
		if os.path.isabs(args[0]):
			build_file = args[0]
		else:
			build_file = os.path.join(cwd, args[0])
		
		target = args [1]
	elif argc == 1:
		target = args[0]
	
	if build_file == None and default_build_file in os.listdir(cwd):
		build_file = os.path.join(cwd, default_build_file) 
	
	ret = pyke.run_build(build_file, target)
	
	if ret:
		sys.ext(ret)

if __name__ == '__main__':
	main()