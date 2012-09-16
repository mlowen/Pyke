import os
import subprocess

from hashlib import md5
from platform import system

def compile_file(output_base_path, file_name, flags, hashes):
	parent_dir = os.path.dirname(file_name)
	base_name = os.path.splitext(os.path.basename(file_name))[0]
	output_path = os.path.join(output_base_path, parent_dir)
	
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	# Create the file hash
	file_hash = md5(open(file_name, 'rb').read()).hexdigest()
	output_file = os.path.join(output_path, '%s.o' % base_name)
	
	if file_name in hashes and hashes[file_name] == file_hash and os.path.exists(output_file):
		print('%s has not changed, will not compile.' % file_name)
	else:
		print('Compiling %s' % file_name)
		hashes[file_name] = file_hash
		
		args = ['g++', '-c', file_name, '-o', output_file] + flags
		subprocess.check_call(args, stderr=subprocess.STDOUT, shell = True)
	
	return output_file

def link_executable(output_path, file_name, object_files, flags, libraries):
	if system().lower() == 'windows':
		file_name = '%s.exe' % file_name
	
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	executable_path = os.path.join(output_path, file_name)
	
	print('Linking %s' % executable_path)
	
	args = ['g++', '-o', executable_path] + object_files + flags + [ '-l%s' %l for l in libraries ]
	
	subprocess.check_call(args, stderr=subprocess.STDOUT, shell = True)