import sys

from . import main

if __name__ == '__main__':
	ret = main('build.py', 'default')
	
	if ret:
		sys.ext(ret)