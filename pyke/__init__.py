import os
import sys
import json
import argparse

from pyke import buildfile
from pyke import compiler
from pyke import target

__version__ = '0.2.0-alpha'

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
	parser = argparse.ArgumentParser(description = 'A C++ build tool.')
	
	parser.add_argument('-t, --target', dest = 'target', 
		metavar = 't', type = str, default = target.get_default_target(), 
		help = 'Target to build, default target is \'%s\'' % target.get_default_target())
	
	parser.add_argument('-f, --file', dest = 'build_file',
		metavar = 'f', type = str, default = buildfile.get_default_filename(),
		help = 'The build file to load, default file name is \'%s\'' % buildfile.get_default_filename())
	
	args = parser.parse_args()
	
	cwd = os.getcwd()
	pyke_path = os.path.join(cwd, '.pyke')
	build_file_path = None
	
	if os.path.isabs(args.build_file):
		build_file_path = args.build_file
	else:
		build_file_path = os.path.join(cwd, args.build_file)
	
	if not os.path.exists(pyke_path):
		os.mkdir(pyke_path)
	
	runner = BuildRunner(buildfile.load(build_file_path), pyke_path)
	ret = None
	
	try:
		runner.run(args.target)
	except Exception as e:
		print('An error occurred while building your project, see above for details.')
		print(e)
		ret = 1		
	
	runner.write_pyke_file()
	
	if not ret == None:
		sys.exit(ret)

if __name__ == '__main__':
	main()