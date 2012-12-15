import os

from fnmatch import fnmatchcase
from pyke import meta

class BaseRunner:
	def __init__(self, build_file, base_path, meta_data = None):
		self.build_file = build_file
		
		if meta_data is not None:
			self.pyke_path = base_path
			self.meta_data = meta_data
		else:
			self.pyke_path = os.path.join(base_path, '.pyke')
			
			if not os.path.exists(self.pyke_path):
				os.mkdir(self.pyke_path)
			
			self.meta_data = meta.MetaFile(os.path.join(self.pyke_path, 'pyke.json'))
		
	def run(self, targets):
		if isinstance(targets, list):
			for t in targets:
				self.run_target(t)
		else:
			self.run_target(targets)
	
	def run_all(self):
		self.run(self.build_file.get_all_targets())
	
	def get_source_files(self, paths, patterns):
		files = [ f for f in paths if os.path.exists(f) and os.path.isfile(f) and True in [ fnmatchcase(f, p) for p in patterns ] ]
		
		for directory in [ d for d in paths if os.path.exists(d) and os.path.isdir(d) ]:
			files += self.get_source_files([ os.path.join(directory, child) for child in os.listdir(directory) ], patterns)
		
		return files
	
	def write_meta_data(self):
		self.meta_data.write()

## Factory ##

from pyke.runners import build
from pyke.runners import clean
from pyke.runners import dependency
from pyke.runners import rebuild

def factory(action, build_file, base_path):
	if action == 'clean':
		return clean.CleanRunner(build_file, base_path)
	elif action == 'dependencies':
		return dependency.DependencyRunner(build_file, base_path)
	elif action == 'rebuild':
		return rebuild.RebuildRunner(build_file, base_path)
	
	return build.BuildRunner(build_file, base_path)