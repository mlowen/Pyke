import os
import subprocess

from platform import system

def compile_file(output_base_path, file_name):
	print('Compiling %s' % file_name)
	
	parent_dir = os.path.dirname(file_name)
	base_name = os.path.splitext(os.path.basename(file_name))[0]
	output_path = os.path.join(output_base_path, parent_dir)
	
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	output_file = os.path.join(output_path, '%s.o' % base_name)
	subprocess.check_call(['g++', '-c', file_name, '-o', output_file], stderr=subprocess.STDOUT, shell = True)
	
	return output_file

def link_executable(output_path, file_name, object_files):
	if system().lower() == 'windows':
		file_name = '%s.exe' % file_name
	
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	executable_path = os.path.join(output_path, file_name)
	
	print('Linking %s' % executable_path)
	
	subprocess.check_call(['g++', '-o', executable_path] + object_files, stderr=subprocess.STDOUT, shell = True)