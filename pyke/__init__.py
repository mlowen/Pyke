from . import buildfile
from . import buildtarget

def create_default_config():
	return None
	
def run_build(filepath, target):
	config = buildtarget.TargetConfig()
	pre_build = None
	post_build = None
	
	if buildfile == None:
		config = create_default_config()
	else:		
		config = buildfile.load(filepath)
	
	print('Build file created')