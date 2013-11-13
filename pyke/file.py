import ctypes
import imp
import inspect
import os
import platform
import sys

import pyke

from pyke import target
from pyke import meta
from pyke import builders

class File(dict):
	def __init__(self, path):
		dict.__init__(self)

		if not os.path.exists(path):
			raise FileNotFoundError(path)

		name, extension = os.path.splitext(path)
		
		# Don't want to create the __pycache__ folder in the users project.
		original_value = sys.dont_write_bytecode
		sys.dont_write_bytecode = True
		
		self.module = imp.load_module(os.path.basename(name), open(path), path, (extension, 'r', imp.PY_SOURCE))

		for method in inspect.getmembers(self.module):
			name = method[0]
			item = inspect.getattr_static(self.module, name)

			if isinstance(item, pyke.TargetWrapper):
				self[name] = item

		sys.dont_write_bytecode = original_value

		self.path = os.path.dirname(path)
		self.meta_path = os.path.join(self.path, '.pyke')

		if not os.path.exists(self.meta_path):
			os.mkdir(self.meta_path)

			if platform.system().lower() == 'windows':
				ctypes.windll.kernel32.SetFileAttributesW(self.meta_path, 2)

		self.meta = meta.File(os.path.join(self.meta_path, 'pyke.json'))
		self.builders = builders.Factory()

	def __getitem__(self, key):
		if key not in self:
			raise pyke.PykeException('No target exists with name %s.' % key)

		t = dict.__getitem__(self, key)

		return target.Target(key, t.fn(), self)

	def targets(self):
		return self.keys()
