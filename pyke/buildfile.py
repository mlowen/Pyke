import imp
import os
import inspect

from . import buildtarget

def get_default_filename():
	return 'build.pyke'

class BuildFileWrapper:
	def __init__(self, module):
		self.module = module
		self.methods = [i[0] for i in inspect.getmembers(self.module) if inspect.isfunction(i[1])]
		
		self.default_prebuild = 'prebuild'
		self.default_postbuild = 'postbuild'
		
		self.prebuild_pattern = 'pre_%s'
		self.postbuild_pattern = 'post_%s'
	
	# Target	
	def target_exists(target):
		return target in self.methods
	
	def run_target(target, config):
		method = getattr(self.module, target)
		
		if method != None:
			method(config)
	
	# Pre-build
	def prebuild_exists(target):
		if target == buildtarget.get_default_target():
			return self.default_prebuild in self.methods
		
		return (self.prebuild_pattern % target) in self.methods
	
	def run_prebuild(target):
		method = None
		
		if target == buildtarget.get_default_target():
			method = getattr(self.module, self.default_prebuild)
		else:
			method = getattr(self.module, (self.prebuild_pattern % target))
		
		if method != None:
			method()
	
	# Post-build
	def postbuild_exists(target):
		if target == buildtarget.get_default_target():
			return self.default_postbuild in self.methods
		
		return (self.postbuild_pattern % target) in self.methods
	
	def run_postbuild(target):
		method = None
		
		if target == buildtarget.get_default_target():
			method = getattr(self.module, self.default_postbuild)
		else:
			method = getattr(self.module, (self.postbuild_pattern % target))
		
		if method != None:
			method()
	

def load(filepath):
	if not os.path.exists(filepath):
		raise Exception('Unable to load build file: %s' % filepath)
	
	fp = open(filepath, 'r')
	filename, extension = os.path.splitext(filepath)
	
	module = imp.load_module(os.path.basename(filename), fp, filepath, (extension, 'r', imp.PY_SOURCE))
	
	fp.close()
	
	return BuildFileWrapper(module)