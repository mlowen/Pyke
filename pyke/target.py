import os
from fnmatch import fnmatchcase

def get_default_target():
	return 'default'

class Config:
	def __init__(self):
		self.paths = None
		self.patterns = None
		self.output_path = None
		self.output_name = None
	
	# Source Files
	def set_source_path(self, paths):
		if isinstance(paths, list):
			self.paths = [ p for p in paths if isinstance(p, str)]
		elif isinstance(paths, str):
			self.paths = [ paths ]
		else:
			raise Exception('Invalid argument, expecting a string or a list')
	
	def get_source_paths(self):
		if self.paths == None or len(self.paths) == 0:
			return [ os.path.relpath(os.getcwd()) ]
		
		return self.paths
			
	def set_source_pattern(self, patterns):
		if isinstance(patterns, list):
			self.patterns = [ p for p in patterns if isinstance(p, str)]
		elif isinstance(patterns, str):
			self.patterns = [ patterns ]
		else:
			raise Exception('Invalid argument, expecting a string or a list')
	
	def get_source_patterns(self):
		if self.patterns == None or len(self.patterns) == 0:
			return [ '*.cc', '*.cpp', '*.cxx' ]
		
		return self.patterns
			
	def get_source_files(self):
		# Parse out the files first
		source_files = [ f for f in self.get_source_paths() if os.path.exists(f) and os.path.isfile(f) ]
		
		for d in [ f for f in self.paths if os.path.exists(f) and os.path.isdir(f) ]:
			source_files.extend(self.get_source_in_directory(d, self.get_source_patterns()))
		
		return source_files
	
	def get_source_in_directory(self, directory, patterns):
		dir_items = os.listdir(directory)
		source_files = [ os.path.join(directory, f) for f in dir_items if os.path.isfile(os.path.join(directory, f)) and True in [ fnmatchcase(f, p) for p in patterns ]]
		
		for sub_dir in [ d for d in dir_items if os.path.isdir(d) ]:
			source_files.extend(self.get_source_in_directory(os.path.join(directory, sub_dir), patterns))
		
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
		
		return os.path.basename(os.path.dirname(os.getcwd()))