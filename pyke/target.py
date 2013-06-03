import os

_defaults = {
	'source_paths': os.getcwd(),
	'source_patterns': None,
	
	'output_path': os.getcwd(),
	'output_name': os.path.basename(os.getcwd()),
	'output_type': 'executable',
	
	'compiler_flags': [],
	'linker_flags': [],
	
	'prebuild': None,
	'postbuild': None,
	'clean': None,
	
	'is_phoney': False,
	'dependencies': None
}

class TargetWrapper:
	def __init__(self, fn):
		self.fn = fn

class Data:
	def __init__(self, data = None):
		self._load_data(_defaults)
		self._load_data(data)
	
	def _load_data(self, data):
		for key in data:
			self.__dict__[key] = data[key]

class Target:
	def __init__(self, name, data, fp):
		self._file = fp
		self._name = name
		self._data = Data(data)

	def build(self, to_build = [], built = []):
		print('Building %s' % self._name)

	def clean(self):
		print('Cleaning %s' % self._name)

	def rebuild(self):
		self.clean()
		self.build()


