import imp
import os
import inspect

from pyke import target

def get_default_filename():
	return 'build.pyke'

class PythonFileWrapper:
	def __init__(self, module):
		self.module = module
		self.methods = [ i[0] for i in inspect.getmembers(self.module) if inspect.isfunction(i[1]) ]
				
		self.prebuild_pattern = 'pre_%s'
		self.postbuild_pattern = 'post_%s'
		
	# Target	
	def target_exists(self, target_name):
		return target_name in self.methods
	
	def run_target(self, target_name):
		method = getattr(self.module, target_name)
		
		if method != None:
			return target.Config(method())
	
	# Pre-build
	def prebuild_exists(self, target_name):
		return (self.prebuild_pattern % target_name) in self.methods
	
	def run_prebuild(self, target_name):
		method = getattr(self.module, (self.prebuild_pattern % target_name))
		
		if method != None:
			method()
	
	# Post-build
	def postbuild_exists(self, target_name):
		return (self.postbuild_pattern % target_name) in self.methods
	
	def run_postbuild(self, target_name):
		method = getattr(self.module, (self.postbuild_pattern % target_name))
		
		if method != None:
			method()
	

def load(filepath):
	if not os.path.exists(filepath):
		raise Exception('Unable to load build file: %s' % filepath)
	
	fp = open(filepath, 'r')
	filename, extension = os.path.splitext(filepath)
	
	module = imp.load_module(os.path.basename(filename), fp, filepath, (extension, 'r', imp.PY_SOURCE))
	
	fp.close()
	
	return PythonFileWrapper(module)