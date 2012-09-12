from . import buildfile
from . import target

def create_default_config():
	return None
	
def run_build(filepath, target_name):
	config = target.Config()
	pre_build = None
	post_build = None
	
	if filepath == None:
		config = create_default_config()
	else:		
		config = buildfile.load(filepath)
	
	print('Build file created')