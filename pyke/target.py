import os
from fnmatch import fnmatchcase

def get_default_target():
	return 'default'

class Config:
	def __init__(self):
		self.paths = []
		self.patterns = []
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
	
	def set_source_regex(self, regex):
		if isinstance(regex, list):
			self.patterns = [ r for r in regex if isinstance(r, str)]
		elif isinstance(regex, str):
			self.patterns = [ regex ]
		else:
			raise Exception('Invalid argument, expecting a string or a list')
	
	def get_source_files(self):
		# Parse out the files first
		source_files = [ f for f in self.paths if os.path.exists(f) and os.path.isfile(f) ]
		
		for d in [ f for f in self.paths if os.path.exists(f) and os.path.isdir(f) ]:
			source_files.extend(self.get_source_in_directory(d))
		
		return source_files
	
	def get_source_in_directory(self, directory):
		dir_items = os.listdir(directory)
		source_files = [ os.path.join(directory, f) for f in dir_items if os.path.isfile(os.path.join(directory, f)) and True in [ fnmatchcase(f, p) for p in self.patterns ]]
		
		for sub_dir in [ d for d in dir_items if os.path.isdir(d) ]:
			source_files.extend(self.get_source_in_directory(os.path.join(directory, sub_dir)))
		
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