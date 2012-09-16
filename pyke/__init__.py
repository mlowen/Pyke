import os
import json

from shutil import rmtree
from tempfile import mkdtemp

from . import buildfile
from . import compiler
from . import target

class BuildRunner:
	def __init__(self, build_file, pyke_path):
		self.build_file = build_file
		self.pyke_path = pyke_path
		self.pyke_file_path = os.path.join(self.pyke_path, 'pyke.json')
		
		if os.path.exists(self.pyke_file_path):
			fp = open(self.pyke_file_path)
			self.pyke_file = json.load(fp)
			fp.close()
		else:
			self.pyke_file = {}
	
	def build_config(self, config, file_hashes):
		# Setup
		tmp_dir = mkdtemp()
		
		try:
			# Compile
			object_files = [ compiler.compile_file(tmp_dir, f, config.compiler_flags, file_hashes) for f in config.get_source_files() ]
	
			# Link
			compiler.link_executable(config.get_output_path(), config.get_output_name(), object_files, config.linker_flags, config.libraries)
		except:
			print('An error occurred while building your project, see above for details.')
			return 1
		
		# Clean up
		rmtree(tmp_dir)
	
	def build_target(self, target_name):
		print('Starting build: %s' % target_name)
		
		if not self.build_file.target_exists(target_name):
			raise Exception('Target %s does not exist.' % target_name)
					
		config = target.Config()
		self.build_file.run_target(target_name, config)
		
		if self.build_file.prebuild_exists(target_name):
			self.build_file.run_prebuild(target_name)
		
		file_hashes = {}
		if target_name in self.pyke_file:
			file_hashes = self.pyke_files[target_name]
			
		if self.build_config(config, file_hashes):
			return 1
		
		if self.build_file.postbuild_exists(target_name):
			self.build_file.run_postbuild(target_name)
		
		print('Successfully built %s' % target_name)
	
	def run(self, target_name):
		if self.build_file == None:
			if self.build_config(target.Config()):
				return 1
		else:			
			if target_name == None:
				target_name = target.get_default_target()
			
			if self.build_target(target_name):
				return 1
	
	def write_pyke_file(self):
		fp = open(self.pyke_file_path, 'w')
		json.dump(self.pyke_file, fp)
		fp.close()