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

class Config:
	def __init__(self, data = None):
		self._load_data(_defaults)
		self._load_data(data)
	
	def _load_data(self, data):
		for key in data:
			self.__dict__[key] = data[key]
