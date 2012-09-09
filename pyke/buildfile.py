import imp
import os

def load(filepath):
	if not os.path.exists(filepath):
		raise Exception('Unable to load build file: %s' % filepath)
	
	fp = open(filepath, 'r')
	filename, extension = os.path.splitext(filepath)
	
	module = imp.load_module(os.path.basename(filename), fp, filepath, (extension, 'r', imp.PY_SOURCE))
	
	fp.close()
	
	return module