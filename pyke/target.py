import os
from fnmatch import fnmatchcase

def get_default_target():
	return 'default'

class Config:
	def __init__(self, data = None):
		if data == None:
			self.data = {}
		else:
			self.data = data
	
	def get_list(self, key):
		if key in self.data:
			if isinstance(self.data[key], list):
				return [ i for i in self.data[key] if isinstance(i, str) ]
			elif isinstance(self.data[key], str):
				return [ self.data[key] ]
		
		return None
		
	def get_source_paths(self):
		paths = self.get_list('source_paths')
		
		return [ os.path.relpath(os.getcwd()) ] if paths == None else paths
	
	def get_source_patterns(self):
		patterns = self.get_list('source_patterns')
		
		return [ '*.cc', '*.cpp', '*.cxx' ] if patterns == None else patterns
	
	def get_source_files(self, paths = None, patterns = None):
		if patterns == None:
			patterns = self.get_source_patterns()
		
		if paths == None:
			paths = self.get_source_paths()
		
		files = [ f for f in paths if os.path.exists(f) and os.path.isfile(f) and True in [ fnmatchcase(f, p) for p in patterns ] ]
		
		for directory in [ d for d in paths if os.path.exists(d) and os.path.isdir(d) ]:
			files += self.get_source_files([ os.path.join(directory, child) for child in os.listdir(directory) ], patterns)
		
		return files
	
	def get_output_path(self):
		key = 'output_path'
		
		return self.data[key] if key in self.data and isinstance(self.data[key], str) else os.getcwd()
		
	def get_output_name(self):
		key = 'output_name'
		
		return self.data[key] if key in self.data and isinstance(self.data[key], str) else os.path.basename(os.getcwd())
	
	def get_compiler_flags(self):
		flags = self.get_list('compiler_flags')
		
		return [] if flags == None else flags
	
	def get_linker_flags(self):
		flags = self.get_list('linker_flags')
		
		return [] if flags == None else flags
	
	def get_libraries(self):
		libraries = self.get_list('libraries')
		
		return [] if libraries == None else libraries
