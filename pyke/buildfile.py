import imp
import os
import inspect
import json
import sys

from pyke import target

class FileWrapperBase:
	def __init__(self):
		self.prebuild_prefix = 'pre_'
		self.postbuild_prefix = 'post_'
		self.clean_prefix = 'clean_'
	
	# Pre-build
	def prebuild_name(self, target_name):
		return '%s%s' % (self.prebuild_prefix, target_name)
	
	# Post-build
	def postbuild_name(self, target_name):
		return '%s%s' % (self.postbuild_prefix, target_name)
	
	# Clean
	def clean_name(self, target):
		return "%s%s" % (self.clean_prefix, target)

class JsonFileWrapper(FileWrapperBase):
	def __init__(self, path):
		FileWrapperBase.__init__(self)
		
		self.data = json.load(open(path, 'r'))
	
	# Target
	def target_exists(self, target_name):
		return target_name in self.data
	
	def run_target(self, target_name):
		return target.Config(self.data[target_name])
	
	def get_all_targets(self):
		return self.data.keys()
	
	# Pre-build
	def prebuild_exists(self, target_name):
		return False
	
	# Post-build
	def postbuild_exists(self, target_name):
		return False
	
	# Clean
	def clean_exists(self, target):
		return False
		
	# Utility Functions
	def method_exists(self, method_name):
		return False

class PythonFileWrapper(FileWrapperBase):
	def __init__(self, path):
		FileWrapperBase.__init__(self)
		
		name, extension = os.path.splitext(path)
		
		# Don't want to created the __pycache__ folder in the users project.
		original_value = sys.dont_write_bytecode
		sys.dont_write_bytecode = True
		
		self.module = imp.load_module(os.path.basename(name), open(path), path, (extension, 'r', imp.PY_SOURCE))
		self.methods = [ i[0] for i in inspect.getmembers(self.module) if inspect.isfunction(i[1]) ]
		
		sys.dont_write_bytecode = original_value
	
	# Target	
	def target_exists(self, target_name):
		return self.method_exists(target_name)
	
	def run_target(self, target_name):
		method = getattr(self.module, target_name)
		
		if method != None:
			return target.Config(method())
	
	def get_all_targets(self):
		return [ m for m in self.methods if not (m.startswith(self.prebuild_prefix) or m.startswith(self.postbuild_prefix) or m.startswith(self.clean_prefix)) ]
	
	# Pre-build
	def prebuild_exists(self, target_name):
		return self.method_exists(self.prebuild_name(target_name))
	
	def run_prebuild(self, target_name):
		self.run_method(self.prebuild_name(target_name))
	
	# Post-build
	def postbuild_exists(self, target_name):
		return self.method_exists(self.postbuild_name(target_name))
	
	def run_postbuild(self, target_name):
		self.run_method(self.postbuild_name(target_name))
	
	# Clean
	def clean_exists(self, target):
		return self.method_exists(self.clean_name(target))
	
	def run_clean(self, target):
		self.run_method(self.clean_name(target))
	
	# Utility Functions
	def method_exists(self, method_name):
		return inspect.isroutine(method_name) or method_name in self.methods
	
	def run_method(self, method_name):
		if inspect.isroutine(method_name):
			method_name()
		else:
			method = getattr(self.module, method_name)
			
			if method != None:
				return method()

def load(filepath):
	if not os.path.exists(filepath):
		raise Exception('Unable to load build file: %s' % filepath)
	
	extension = os.path.splitext(filepath)[1]
	
	build_file = None
	
	if extension == '.pyke':
		build_file = PythonFileWrapper(filepath)
	elif extension == '.json':
		build_file = JsonFileWrapper(filepath)
	
	return build_file