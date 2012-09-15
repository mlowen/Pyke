import os
from fnmatch import fnmatchcase

def get_default_target():
	return 'default'

def set_list(items):
	if isinstance(items, list):
		return [ i for i in items if isinstance(i, str)]
	elif isinstance(items, str):
		return [ items ]
	else:
		raise Exception('Invalid argument, expecting a string or a list')
	
class Config:
	def __init__(self):
		self.paths = None
		self.patterns = None
		self.output_path = None
		self.output_name = None
		self.compiler_flags = []
		self.linker_flags = []
		self.libraries = []
		
	# Source Files
	def set_source_path(self, paths):
		self.paths = set_list(paths)
	
	def get_source_paths(self):
		if self.paths == None or len(self.paths) == 0:
			return [ os.path.relpath(os.getcwd()) ]
		
		return self.paths
			
	def set_source_pattern(self, patterns):
		self.patterns = set_list(patterns)
	
	def get_source_patterns(self):
		if self.patterns == None or len(self.patterns) == 0:
			return [ '*.cc', '*.cpp', '*.cxx' ]
		
		return self.patterns
			
	def get_source_files(self):
		paths = self.get_source_paths()
		
		# Parse out the files first
		source_files = [ f for f in paths if os.path.exists(f) and os.path.isfile(f) ]
		
		for d in [ f for f in paths if os.path.exists(f) and os.path.isdir(f) ]:
			source_files.extend(self.get_source_in_directory(d, self.get_source_patterns()))
		
		return source_files
	
	def get_source_in_directory(self, directory, patterns):
		dir_items = os.listdir(directory)
		source_files = [ os.path.join(directory, f) for f in dir_items if os.path.isfile(os.path.join(directory, f)) and True in [ fnmatchcase(f, p) for p in patterns ]]
		
		for sub_dir in [ os.path.join(directory, d) for d in dir_items if os.path.isdir(os.path.join(directory, d)) ]:
			source_files.extend(self.get_source_in_directory(sub_dir, patterns))
		
		return source_files
	
	# Output
	def set_output_path(self, path):
		self.output_path = path
	
	def get_output_path(self):
		if self.output_path != None and isinstance(self.output_path, str):
			return self.output_path
		
		return os.getcwd()
		
	def set_output_name(self, name):
		self.output_name = name
	
	def get_output_name(self):
		if self.output_name != None and isinstance(self.output_name, str):
			return self.output_name
		
		return os.path.basename(os.getcwd())
	
	def set_compiler_flags(self, flags):
		self.compiler_flags = set_list(flags)
	
	def set_linker_flags(self, flags):
		self.linker_flags = set_list(flags)
	
	def set_libraries(self, libraries):
		self.libraries = set_list(libraries)