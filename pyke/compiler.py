import os
import subprocess

from hashlib import md5
from platform import system

def get_output_name(base_name, output_type):
	if output_type == 'executable' and system().lower() == 'windows':
		return '%s.exe' % base_name
	elif output_type == 'sharedlib':
		return'%s.a' % base_name
	elif output_type == 'dynamiclib':
		if system().lower() == 'windows':
			return '%s.dll' % base_name
		else:
			return '%s.so' % base_name
	elif not output_type == 'executable':
		raise Exception('Unknown output type: %s' % output_type)
					
	return base_name

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

def link_executable(output_path, file_name, object_files, flags):
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	executable_path = os.path.join(output_path, file_name)
	
	print('Linking %s' % executable_path)
	
	args = ['g++', '-o', executable_path] + object_files + flags
	
	subprocess.check_call(args, stderr=subprocess.STDOUT, shell = True)

def link_static_library(output_path, file_name, object_files):
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	executable_path = os.path.join(output_path, file_name)
	
	print('Linking %s' % executable_path)
	
	args = ['ar', 'crf', executable_path ] + object_files + flags
	
	subprocess.check_call(args, stderr = subprocess.STDOUT, shell = True)

def link_dynamic_library(output_path, file_name, object_files, flags):
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	
	executable_path = os.path.join(output_path, file_name)
	
	print('Linking %s' % executable_path)
	
	args = [ 'g++', '-shared', '-o', executable_path ] + object_files + flags
	
	subprocess.check_call(args, stderr = subprocess.STDOUT, shell = True)