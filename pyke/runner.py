import os
import json

from pyke import compiler
from pyke import target

class BuildRunner:
	def __init__(self, build_file, base_path):
		self.build_file = build_file
		self.pyke_path = os.path.join(base_path, '.pyke')
		self.pyke_file_path = os.path.join(self.pyke_path, 'pyke.json')
		
		if not os.path.exists(self.pyke_path):
			os.mkdir(self.pyke_path)
		
		if os.path.exists(self.pyke_file_path):
			self.pyke_file = json.load(open(self.pyke_file_path))
		else:
			self.pyke_file = {}
	
	def build(self, target_name):
		print('Starting build: %s' % target_name)
		
		if not self.build_file.target_exists(target_name):
			raise Exception('Target %s does not exist.' % target_name)
					
		config = self.build_file.run_target(target_name)
		
		if self.build_file.prebuild_exists(target_name):
			self.build_file.run_prebuild(target_name)
		
		# Setup
		obj_dir = os.path.join(self.pyke_path, target_name)
		hashes = self.pyke_file[target_name] if target_name in self.pyke_file else {}
		
		# Compile
		object_files = [ compiler.compile_file(obj_dir, f, config.get_compiler_flags(), hashes) for f in config.get_source_files() ]
		
		# Link
		compiler.link_executable(config.get_output_path(), config.get_output_name(), object_files, config.get_linker_flags(), config.get_libraries())
		
		self.pyke_file[target_name] = hashes
		
		if self.build_file.postbuild_exists(target_name):
			self.build_file.run_postbuild(target_name)
		
		print('Successfully built %s' % target_name)
		
	def write_pyke_file(self):
		fp = open(self.pyke_file_path, 'w')
		json.dump(self.pyke_file, fp)
		fp.close()