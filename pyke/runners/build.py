import os

from pyke import compilers
from pyke.runners import BaseRunner

class BuildRunner(BaseRunner):
    def __init__(self, build_file, base_path, meta_data = None):
        BaseRunner.__init__(self, build_file, base_path, meta_data)
        
    def run_target(self, target_name):
        print('Starting build: %s' % target_name)
        
        if not self.build_file.target_exists(target_name):
            raise Exception('Target %s does not exist.' % target_name)
        
        self.meta_data.set_target(target_name)
        config = self.build_file.run_target(target_name)
        
        if config.prebuild is not None and self.build_file.method_exists(config.prebuild):
            self.build_file.run_method(config.prebuild)
        elif self.build_file.prebuild_exists(target_name):
            self.build_file.run_prebuild(target_name)
        
        if config.is_phoney and self.build_file.method_exists(config.run):
            self.build_file.run_method(config.run)
        elif not config.is_phoney:
            # Setup
            compiler = compilers.factory(config.compiler, config.output_type)
            compiler.set_object_directory(os.path.join(self.pyke_path, target_name))
            
            # Compile
            object_files = self.compile(config, compiler)
            
            # Link
            self.link(config, compiler, object_files)
        
        if config.postbuild is not None and self.build_file.method_exists(config.postbuild):
            self.build_file.run_method(config.postbuild)
        elif self.build_file.postbuild_exists(target_name):
            self.build_file.run_postbuild(target_name)
        
        print('Successfully built %s' % target_name)
        
    def compile(self, config, compiler):
        source_patterns = config.source_patterns
        
        if source_patterns is None:
            source_patterns = compiler.get_source_patterns()
        
        source_files = self.get_source_files(config.source_paths, source_patterns)
        object_files = []
        
        for f in source_files:
            object_file = compiler.get_object_file_name(f)
            
            if self.meta_data.has_file_changed(f) or not os.path.exists(object_file):
                print('Compiling %s' % f)
                compiler.compile(f, config.compiler_flags)
            else:
                print('%s has not changed, will not compile.' % f)
            
            object_files.append(object_file)
        
        return object_files
    
    def link(self, config, compiler, object_files):
        output_name = compiler.get_output_name(config.output_name)
        
        print('Linking %s' % output_name)
        
        if not os.path.exists(config.output_path):
            os.makedirs(config.output_path)
                    
        compiler.link(os.path.join(config.output_path, output_name), object_files, config.linker_flags)