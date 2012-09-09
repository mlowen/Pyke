import os.path
import pyke.buildfile

class BuildConfig:
	def __init__(self):
		self.paths = []
		self.build_system = ''
	
	def set_source_path(paths):
		if isinstance(paths, list):
			self.paths = [ p for p in paths if isinstance(p, str)]
		elif isinstance(paths, str):
			self.paths = [ paths ]
		else:
			raise Exception('Invalid object passed to set_source_paths, expecting a string or an array')
	
	def set_build_system(builder):
		self.build_system = builder

def create_default_config():
	return None
		
def run_build(filepath, target):
	config = BuildConfig()
	pre_build = None
	post_build = None
	
	if buildfile == None:
		config = create_default_config()
	else:		
		config = buildfile.load(filepath)
	
	print('Build file created')