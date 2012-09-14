import os
from shutil import rmtree
from tempfile import mkdtemp

from . import buildfile
from . import compiler
from . import target

def create_default_config():
	return None
	
def run_build(filepath, target_name):
	config = None
	build_file = None
	
	if filepath == None:
		config = target.Config()	
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
	
	# Setup
	tmp_dir = mkdtemp()
	
	try:
		# Compile
		object_files = [ compiler.compile_file(tmp_dir, f) for f in config.get_source_files() ]		
	
		# Link
		compiler.link_executable(config.get_output_path(), config.get_output_name(), object_files)
	except:
		print('An error occurred while building your project, see above for details.')
		return 1
		
	
	# Clean up
	rmtree(tmp_dir)