import os

from . import buildfile
from . import target

def create_default_config():
	return None
	
def run_build(filepath, target_name):
	if not os.path.exists(filepath):
		raise Exception('Unable to find build file: %s' % filepath)
	
	build_file = buildfile.load(filepath)
	
	if target_name == None:
		target_name = target.get_default_target()
	
	if not build_file.target_exists(target_name):
		raise Exception('Target %s does not exist.' % target_name)
	
	config = target.Config()
	
	build_file.run_target(target_name, config)
	
	print(config.paths)