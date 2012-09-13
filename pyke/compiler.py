import subprocess
import os

def compile_file(output_base_dir, file_name):
	print('Compiling %s' % file_name)
	
	parent_dir = os.path.dirname(file_name)
	base_name = os.path.splitext(os.path.basename(file_name))[0]
	output_dir = os.path.join(output_base_dir, parent_dir)
	
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	
	output_file = os.path.join(output_dir, '%s.o' % base_name)
	
	subprocess.check_call(['g++', '-c', file_name, '-o', output_file], stderr=subprocess.STDOUT, shell = True)
	
	return output_file