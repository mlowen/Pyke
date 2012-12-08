# g++ compiler classes
import os
import subprocess

from hashlib import md5
from platform import system

class BaseCompiler:
    def __init__(self):
        self.obj_dir = ''
    
    def compile(self, file_name, flags):
        output_file = self.get_object_file_name(file_name)
        output_path = os.path.dirname(output_file)
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        args = ['g++', '-c', file_name, '-o', output_file] + flags
        subprocess.check_call(args, stderr=subprocess.STDOUT, shell = True)
    
    def get_object_file_name(self, file_name):
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        parent_dir = os.path.dirname(file_name)
        output_path = os.path.join(self.obj_dir, parent_dir)
        
        return os.path.join(output_path, '%s.o' % base_name)
    
    def get_source_patterns(self):
        return [ '*.cc', '*.cpp', '*.cxx' ]
    
    def set_object_directory(self, obj_dir):
        self.obj_dir = obj_dir
        
        if not os.path.exists(self.obj_dir):
            os.makedirs(self.obj_dir)

class ExecutableCompiler(BaseCompiler):
    def get_output_name(self, base_name):
        if system().lower() == 'windows':
            return '%s.exe' % base_name
        
        return base_name
    
    def link(self, output_path, file_name, object_files, flags):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        executable_path = os.path.join(output_path, file_name)
        
        print('Linking %s' % executable_path)
        
        args = ['g++', '-o', executable_path] + object_files + flags
        
        subprocess.check_call(args, stderr=subprocess.STDOUT, shell = True)

class StaticLibraryCompiler(BaseCompiler):
    def get_output_name(self, base_name):
        return'%s.a' % base_name
    
    def link(self, output_path, file_name, object_files, flags):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        executable_path = os.path.join(output_path, file_name)
        
        print('Linking %s' % executable_path)
        
        args = ['ar', 'crf', executable_path ] + object_files + flags
        
        subprocess.check_call(args, stderr = subprocess.STDOUT, shell = True)

class DynamicLibraryCompiler(BaseCompiler):
    def get_output_name(self, base_name):
        if system().lower() == 'windows':
            return '%s.dll' % base_name
        else:
            return '%s.so' % base_name
    
    def link(self, output_path, file_name, object_files, flags):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        executable_path = os.path.join(output_path, file_name)
        
        print('Linking %s' % executable_path)
        
        args = [ 'g++', '-shared', '-o', executable_path ] + object_files + flags
        
        subprocess.check_call(args, stderr = subprocess.STDOUT, shell = True)