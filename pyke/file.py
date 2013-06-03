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

		if not os.path.exists(path):
			raise FileNotFoundError(path)

		name, extension = os.path.splitext(path)
		
		# Don't want to created the __pycache__ folder in the users project.
		original_value = sys.dont_write_bytecode
		sys.dont_write_bytecode = True
		
		self.module = imp.load_module(os.path.basename(name), open(path), path, (extension, 'r', imp.PY_SOURCE))

		for method in inspect.getmembers(self.module):
			name = method[0]
			item = inspect.getattr_static(self.module, name)

			if isinstance(item, pyke.TargetWrapper):
				self[name] = item

		sys.dont_write_bytecode = original_value
	
	def __getitem__(self, key):
		t = dict.__getitem__(self, key)

		return target.Target(key, t.fn(), self)

	def targets(self):
		return self.keys()
