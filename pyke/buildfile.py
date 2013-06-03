import imp
import os
import inspect
import json
import sys

import pyke

from pyke import target

class File(dict):
	def __init__(self, path):
		dict.__init__(self)
		
		self.prebuild_prefix = 'pre_'
		self.postbuild_prefix = 'post_'
		self.clean_prefix = 'clean_'

		if not os.path.exists(path):
			raise FileNotFoundError(path)

		name, extension = os.path.splitext(path)
		
		# Don't want to created the __pycache__ folder in the users project.
		original_value = sys.dont_write_bytecode
		sys.dont_write_bytecode = True
		
		self.module = imp.load_module(os.path.basename(name), open(path), path, (extension, 'r', imp.PY_SOURCE))
		self.methods = [ i[0] for i in inspect.getmembers(self.module) if inspect.isfunction(i[1]) ]
		
		for method in inspect.getmembers(self.module):
			name = method[0]
			item = inspect.getattr_static(self.module, name)

			if isinstance(item, pyke.TargetWrapper):
				self[name] = item

		sys.dont_write_bytecode = original_value
	
	def __getitem__(self, key):
		t = dict.__getitem__(self, key)

		return target.Config(t.fn())

	def targets(self):
		return self.keys()

	# Existing functionality

	# Pre-build
	def prebuild_name(self, target_name):
		return '%s%s' % (self.prebuild_prefix, target_name)

	# Post-build
	def postbuild_name(self, target_name):
		return '%s%s' % (self.postbuild_prefix, target_name)

	# Clean
	def clean_name(self, target):
		return "%s%s" % (self.clean_prefix, target)

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
