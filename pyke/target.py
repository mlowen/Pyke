import re

def get_default_target():
	return 'default'

class Config:
	def __init__(self):
		self.paths = []
		self.regexs = []
	
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
			self.regexs = [ re.compile(r) for r in regex if isinstance(r, str)]
		elif isinstance(regex, str):
			self.regexs = [ re.compile(regex) ]
		else:
			raise Exception('Invalid argument, expecting a string or a list')