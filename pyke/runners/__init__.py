import os
import json
import shutil

from fnmatch import fnmatchcase
from platform import system

from pyke import compilers
from pyke import meta

class BaseRunner:
	def __init__(self, build_file, base_path):
		self.build_file = build_file
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

from pyke.runners import build

def factory(action, build_file, base_path):
	if action == 'clean':
		return CleanRunner(build_file, base_path)
	elif action == 'dependencies':
		return DependencyRunner(build_file, base_path)
	
	return build.BuildRunner(build_file, base_path)

class CleanRunner(BaseRunner):
	def __init__(self, build_file, base_path):
		BaseRunner.__init__(self, build_file, base_path)
	
	def run_target(self, target_name):
		print('Starting clean: %s' % target_name)
		
		if not self.build_file.target_exists(target_name):
			raise Exception('Target %s does not exist.' % target_name)
		
		# Delete pyke generated  intermediate files
		self.meta_data.delete_target(target_name)
		obj_dir = os.path.join(self.pyke_path, target_name)
		
		if(os.path.exists(obj_dir)):
			shutil.rmtree(obj_dir)
		
		config = self.build_file.run_target(target_name)
		compiler = compilers.factory(config.get_compiler(), config.get_output_type())
		custom_clean = config.get_clean()
		
		# Check if the build file has a custom clean available.
		if not custom_clean == None and self.build_file.method_exists(custom_clean):
			self.build_file.run_method(custom_clean)
		elif self.build_file.clean_exists(target_name):
			self.build_file.run_clean(target_name)
		else:
			output_path = config.get_output_path()
			
			if os.path.exists(output_path) and not os.getcwd() == output_path:
				shutil.rmtree(output_path)
			else:
				output_type = config.get_output_type()
				output_name = compiler.get_output_name(config.get_output_name())
				
				if os.path.exists(output_name):
					os.remove(output_name)
					
		print('Successfully cleaned %s' % target_name)

class DependencyRunner(BaseRunner):
	def __init__(self, build_file, base_path):
		BaseRunner.__init__(self, build_file, base_path)
	
	def run_target(self, target_name):
		print('Generating file dependencies for %s' % target_name)
		
		if not self.build_file.target_exists(target_name):
			raise Exception('Target %s does not exist.' % target_name)
		
		self.meta_data.set_target(target_name)
		config = self.build_file.run_target(target_name)
		compiler = compilers.factory(config.get_compiler(), config.get_output_type())
		
		source_paths = config.get_source_paths();
		source_patterns = config.get_source_patterns();
		
		if source_patterns is None:
			source_patterns = compiler.get_source_patterns()
		
		source_files = self.get_source_files(source_paths, source_patterns)
		
		for f in source_files:
			self.meta_data.set_file_dependencies(f, compiler.get_file_dependencies(f))
		
		print('Successfully generated file dependencies for %s' % target_name)