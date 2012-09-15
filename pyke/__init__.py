import os
from shutil import rmtree
from tempfile import mkdtemp

from . import buildfile
from . import compiler
from . import target

def build_config(config):
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

def build_target(build_file, target_name, config):
	print('Starting build: %s' % target_name)
	
	if build_config(config):
		return 1
	
	print('Successfully built %s' % target_name)
	
def run_build(filepath, target_name):
	config = None
	build_file = None
	
	if filepath == None:
		if build_config(target.Config()):
			return 1
	else:
		if not os.path.exists(filepath):
			raise Exception('Unable to find build file: %s' % filepath)
		
		build_file = buildfile.load(filepath)
		
		if target_name == None:
			target_name = target.get_default_target()
	
		if not build_file.target_exists(target_name):
			raise Exception('Target %s does not exist.' % target_name)
		
		config = target.Config()
		build_file.run_target(target_name, config)
		
		if build_target(build_file, target_name, config):
			return 1