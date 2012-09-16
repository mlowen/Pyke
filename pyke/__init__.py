import os
from shutil import rmtree
from tempfile import mkdtemp

from . import buildfile
from . import compiler
from . import target

class BuildRunner:
	def __init__(self, build_file):
		self.build_file = build_file
	
	def build_config(self, config):
		# Setup
		tmp_dir = mkdtemp()
		
		try:
			# Compile
			object_files = [ compiler.compile_file(tmp_dir, f, config.compiler_flags) for f in config.get_source_files() ]
	
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
		
		if self.build_config(config):
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