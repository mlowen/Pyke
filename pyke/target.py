import os
from fnmatch import fnmatchcase

class Config:
	def __init__(self, data = None):
		if data is None:
			self.data = {}
		else:
			self.data = data
	
	def get_list(self, key, default):
		if key in self.data:
			if isinstance(self.data[key], list):
				return [ i for i in self.data[key] if isinstance(i, str) ]
			elif isinstance(self.data[key], str):
				return [ self.data[key] ]
		
		return default
	
	def get_string(self, key, default):
		return self.data[key] if key in self.data and isinstance(self.data[key], str) else default
	
	def get_compiler(self):
		return self.get_string('compiler', 'g++')
		
	def get_source_paths(self):
		return self.get_list('source_paths', os.getcwd())
	
	def get_source_patterns(self):
		 return self.get_list('source_patterns', [ '*.cc', '*.cpp', '*.cxx' ])
	
	def get_source_files(self, paths = None, patterns = None):
		if patterns is None:
			patterns = self.get_source_patterns()
		
		if paths is None:
			paths = self.get_source_paths()
		
		files = [ f for f in paths if os.path.exists(f) and os.path.isfile(f) and True in [ fnmatchcase(f, p) for p in patterns ] ]
		
		for directory in [ d for d in paths if os.path.exists(d) and os.path.isdir(d) ]:
			files += self.get_source_files([ os.path.join(directory, child) for child in os.listdir(directory) ], patterns)
		
		return files
	
	def get_output_path(self):
		return self.get_string('output_path', os.getcwd())
		
	def get_output_name(self):
		return self.get_string('output_name', os.path.basename(os.getcwd()))
	
	def get_output_type(self):
		return self.get_string('output_type', 'executable').strip().lower()
	
	def get_compiler_flags(self):
		return self.get_list('compiler_flags', [])
	
	def get_linker_flags(self):
		return self.get_list('linker_flags', [])
		
	def get_prebuild(self):
		return self.get_string('prebuild', None)
		
	def get_postbuild(self):
		return self.get_string('postbuild', None)
	
	def get_clean(self):
		return self.get_string('clean', None)