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
		
		self.prebuild_prefix = 'pre_'
		self.postbuild_prefix = 'post_'
		
	# Target	
	def target_exists(self, target_name):
		return self.method_exists(target_name)
	
	def run_target(self, target_name):
		method = getattr(self.module, target_name)
		
		if method != None:
			return target.Config(method())
	
	def get_all_targets(self):
		return [ m for m in self.methods if not (m.startswith(self.prebuild_prefix) or m.startswith(self.postbuild_prefix)) ]
	
	# Pre-build
	def prebuild_name(self, target_name):
		return '%s%s' % (self.prebuild_prefix, target_name)
	
	def prebuild_exists(self, target_name):
		return self.method_exists(self.prebuild_name(target_name))
	
	def run_prebuild(self, target_name):
		self.run_method(prebuild_name(target_name))
	
	# Post-build
	def postbuild_name(self, target_name):
		return '%s%s' % (self.postbuild_prefix, target_name)
	
	def postbuild_exists(self, target_name):
		return self.method_exists(self.postbuild_name(target_name))
	
	def run_postbuild(self, target_name):
		self.run_method(self.postbuild_name(target_name))
	
	# Utility Functions
	def method_exists(self, method_name):
		return method_name in self.methods
	
	def run_method(self, method_name):
		method = getattr(self.module, method_name)
		
		if method != None:
			return method()

def load(filepath):
	if not os.path.exists(filepath):
		raise Exception('Unable to load build file: %s' % filepath)
	
	fp = open(filepath, 'r')
	filename, extension = os.path.splitext(filepath)
	
	module = imp.load_module(os.path.basename(filename), fp, filepath, (extension, 'r', imp.PY_SOURCE))
	
	fp.close()
	
	return PythonFileWrapper(module)