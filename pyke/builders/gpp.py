import os
import re
import subprocess

from platform import system
from collections import deque

NAME = 'g++'

def factory(output_type):
	if output_type == 'executable':
		return ExecutableCompiler()
	elif output_type == 'sharedlib':
		return StaticLibraryCompiler()
	elif output_type == 'dynamiclib':
		return DynamicLibraryCompiler()
	
	return None

class BaseCompiler:
	def __init__(self):
		self._object_directory = ''
		self._dependency_regex = re.compile('#include \"([^\"]+)\"')
		self.has_linker = True
		self.patterns = [ '*.c', '*.cpp', '*.cxx' ]
	
	def compile(self, file_name, flags):
		output_file = self.object_file_name(file_name)
		output_path = os.path.dirname(output_file)
		
		if not os.path.exists(output_path):
			os.makedirs(output_path)
		
		args = ['g++', '-c', file_name, '-o', output_file] + flags
		subprocess.check_call(args, stderr=subprocess.STDOUT, shell = True)
	
	def object_file_name(self, file_name):
		base_name = os.path.splitext(os.path.basename(file_name))[0]
		parent_dir = os.path.dirname(file_name)
		output_path = os.path.join(self._object_directory, parent_dir)
		
		return os.path.join(output_path, '%s.o' % base_name)
	
	def dependencies(self, file_name):
		fp = open(file_name, 'r')
		parent_dir = os.path.dirname(file_name)
		
		results = self._dependency_regex.search(fp.read())
		dependencies = []

		if results is not None:
			for header in [ os.path.normpath(os.path.join(parent_dir, f)) for f in results.groups() ]:
				dependencies.append(header)
				
				hp = open(header, 'r')
				
				header_results = self._dependency_regex.search(hp.read())
				
				if header_results is not None:
					header_parent = os.path.dirname(header)
					dependencies.extend([ os.path.normpath(os.path.join(header_parent, h)) for h in header_results.groups() ])
				
				hp.close()

		return dependencies
	
	def object_directory(self, obj_dir):
		self._object_directory = obj_dir
		
		if not os.path.exists(self._object_directory):
			os.makedirs(self._object_directory)

class ExecutableCompiler(BaseCompiler):
	def output_name(self, base_name):
		if system().lower() == 'windows':
			return '%s.exe' % base_name
		
		return base_name
	
	def link(self, executable_path, object_files, flags):
		args = ['g++', '-o', executable_path] + object_files + flags
		
		subprocess.check_call(args, stderr=subprocess.STDOUT, shell = True)

class StaticLibraryCompiler(BaseCompiler):
	def output_name(self, base_name):
		return'%s.a' % base_name
	
	def link(self, executable_path, object_files, flags):
		args = ['ar', 'crf', executable_path ] + object_files + flags
		
		subprocess.check_call(args, stderr = subprocess.STDOUT, shell = True)

class DynamicLibraryCompiler(BaseCompiler):
	def output_name(self, base_name):
		if system().lower() == 'windows':
			return '%s.dll' % base_name
		else:
			return '%s.so' % base_name
	
	def link(self, executable_path, object_files, flags):
		args = [ 'g++', '-shared', '-o', executable_path ] + object_files + flags
		
		subprocess.check_call(args, stderr = subprocess.STDOUT, shell = True)