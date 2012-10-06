import os
import sys
import json

from pyke import buildfile
from pyke import compiler
from pyke import target

__version__ = '0.1.1-alpha'

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
	
	def build_config(self, name, config):
		# Setup
		obj_dir = os.path.join(self.pyke_path, name)
		hashes = self.pyke_file[name] if name in self.pyke_file else {}
		
		# Compile
		object_files = [ compiler.compile_file(obj_dir, f, config.get_compiler_flags(), hashes) for f in config.get_source_files() ]
		
		# Link
		compiler.link_executable(config.get_output_path(), config.get_output_name(), object_files, config.get_linker_flags(), config.get_libraries())
		
		self.pyke_file[name] = hashes
	
	def build_target(self, target_name):
		print('Starting build: %s' % target_name)
		
		if not self.build_file.target_exists(target_name):
			raise Exception('Target %s does not exist.' % target_name)
					
		config = self.build_file.run_target(target_name)
		
		if self.build_file.prebuild_exists(target_name):
			self.build_file.run_prebuild(target_name)
		
		self.build_config(target_name, config)
		
		if self.build_file.postbuild_exists(target_name):
			self.build_file.run_postbuild(target_name)
		
		print('Successfully built %s' % target_name)
	
	def run(self, target_name):
		if self.build_file == None:
			self.build_config(target.get_default_target(), target.Config())
		else:			
			if target_name == None:
				target_name = target.get_default_target()
			
			self.build_target(target_name)
	
	def write_pyke_file(self):
		fp = open(self.pyke_file_path, 'w')
		json.dump(self.pyke_file, fp)
		fp.close()

def main():
	args = sys.argv[1:]
	argc = len(args)
		
	cwd = os.getcwd()
	default_build_file = buildfile.get_default_filename()
	pyke_path = os.path.join(cwd, '.pyke')
	build_file = None
	build_file_path = None
	target = None
	
	# This needs to be rewritten to have proper argument parsing
	if argc == 2: # We have both the build script and target specified
		if os.path.isabs(args[0]):
			build_file_path = args[0]
		else:
			build_file_path = os.path.join(cwd, args[0])
		
		target = args[1]
	elif argc == 1:
		target = args[0]
	
	if build_file_path == None and default_build_file in os.listdir(cwd):
		build_file_path = os.path.join(cwd, default_build_file) 
	
	if not build_file_path == None:
		build_file = buildfile.load(build_file_path)
	
	if not os.path.exists(pyke_path):
		os.mkdir(pyke_path)
	
	runner = BuildRunner(build_file, pyke_path)
	ret = None
	
	try:
		runner.run(target)
	except Exception as e:
		print('An error occurred while building your project, see above for details.')
		print(e)
		ret = 1		
	
	runner.write_pyke_file()
	
	if not ret == None:
		sys.exit(ret)

if __name__ == '__main__':
	main()