# g++ compiler classes
import os
import subprocess

from hashlib import md5
from platform import system

class BaseCompiler:
    def linker_stage(self):
        return True
    
    def compile(self, output_base_path, files, flags, hashes):
        object_files = []
        
        for f in files:
            parent_dir = os.path.dirname(f)
            base_name = os.path.splitext(os.path.basename(f))[0]
            output_path = os.path.join(output_base_path, parent_dir)
            
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            # Create the file hash
            file_hash = md5(open(f, 'rb').read()).hexdigest()
            output_file = os.path.join(output_path, '%s.o' % base_name)
            
            if file_name in hashes and hashes[f] == file_hash and os.path.exists(output_file):
                print('%s has not changed, will not compile.' % file_name)
            else:
                print('Compiling %s' % f)
                hashes[file_name] = file_hash
                
                args = ['g++', '-c', f, '-o', output_file] + flags
                subprocess.check_call(args, stderr=subprocess.STDOUT, shell = True)
            
            object_files.append(object_file)
        
        return object_files

class ExecutableCompiler(BaseCompiler):
    def get_ouput_name(self, base_name):
        if output_type == 'executable' and system().lower() == 'windows':
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