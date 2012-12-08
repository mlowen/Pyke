import os
import json
import shutil

from platform import system
from pyke import compiler
from pyke import target

class BaseRunner:
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
	
	def write_pyke_file(self):
		fp = open(self.pyke_file_path, 'w')
		json.dump(self.pyke_file, fp)
		fp.close()

class BuildRunner(BaseRunner):
	def __init__(self, build_file, base_path):
		BaseRunner.__init__(self, build_file, base_path)
		
	def build(self, targets):
		if isinstance(targets, list):
			for t in targets:
				self.build(t)
		else:
			target_name = targets
			print('Starting build: %s' % target_name)
			
			if not self.build_file.target_exists(target_name):
				raise Exception('Target %s does not exist.' % target_name)
			
			config = self.build_file.run_target(target_name)
			
			custom_prebuild = config.get_prebuild()
			
			if not custom_prebuild == None and self.build_file.method_exists(custom_prebuild):
				self.build_file.run_method(custom_prebuild)
			elif self.build_file.prebuild_exists(target_name):
				self.build_file.run_prebuild(target_name)
			
			# Setup
			obj_dir = os.path.join(self.pyke_path, target_name)
			hashes = self.pyke_file[target_name] if target_name in self.pyke_file else {}
			
			# Compile
			object_files = [ compiler.compile_file(obj_dir, f, config.get_compiler_flags(), hashes) for f in config.get_source_files() ]
			
			# Link
			output_type = config.get_output_type()
			output_name = config.get_output_name()			
			
			if output_type == 'executable':
				if system().lower() == 'windows':
					output_name = '%s.exe' % output_name
	
				compiler.link_executable(config.get_output_path(), output_name, object_files, config.get_linker_flags(), config.get_libraries())
			elif output_type == 'sharedlib':
				compiler.link_static_library(config.get_output_path(), '%.a' % output_name, object_files, config.get_linker_flags(), config.get_libraries())
			elif output_type == 'dynamiclib':
				if system().lower() == 'windows':
					output_name = '%s.dll' % output_name
				else:
					output_name = '%s.so' % output_name
				
				compiler.link_dynamic_library(config.get_output_path(), output_name, object_files, config.get_linker_flags(), config.get_libraries())
			else:
				raise Exception('Unknown output type: %s' % output_type)
			
			self.pyke_file[target_name] = hashes
			
			custom_postbuild = config.get_postbuild()
			
			if not custom_postbuild == None and self.build_file.method_exists(custom_postbuild):
				self.build_file.run_method(custom_postbuild)
			elif self.build_file.postbuild_exists(target_name):
				self.build_file.run_postbuild(target_name)
			
			print('Successfully built %s' % target_name)
	
	def build_all(self):
		self.build(self.build_file.get_all_targets())
			
	def clean(self, targets):
		if isinstance(targets, list):
			for t in targets:
				self.clean(t)
		else:
			target_name = targets
			print('Starting clean: %s' % target_name)
			
			if not self.build_file.target_exists(target_name):
				raise Exception('Target %s does not exist.' % target_name)
			
			# Delete pyke generated  intermediate files
			if target_name in self.pyke_file:
				del self.pyke_file[target_name]
				
			obj_dir = os.path.join(self.pyke_path, target_name)
			
			if(os.path.exists(obj_dir)):
				shutil.rmtree(obj_dir)
			
			config = self.build_file.run_target(target_name)
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
					output_name = config.get_output_name()
					
					if output_type == 'executable' and system().lower() == 'windows':
						output_name = '%s.exe' % output_name
					elif output_type == 'sharedlib':
						output_name = '%s.a'
					elif output_type == 'dynamiclib':
						if system().lower() == 'windows':
							output_name = '%s.dll' % output_name
						else:
							output_name = '%s.so' % output_name
					elif not output_type == 'executable':
						raise Exception('Unknown output type: %s' % output_type)
					
					if os.path.exists(output_name):
						os.remove(output_name)
						
			print('Successfully cleaned %s' % target_name)
	
	def clean_all(self):
		self.clean(self.build_file.get_all_targets())