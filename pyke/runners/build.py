import os

from pyke import compilers
from pyke.runners import BaseRunner

class BuildRunner(BaseRunner):
    def __init__(self, build_file, base_path):
        BaseRunner.__init__(self, build_file, base_path)
        
    def run_target(self, target_name):
        print('Starting build: %s' % target_name)
        
        if not self.build_file.target_exists(target_name):
            raise Exception('Target %s does not exist.' % target_name)
        
        self.meta_data.set_target(target_name)
        config = self.build_file.run_target(target_name)
        compiler = compilers.factory(config.get_compiler(), config.get_output_type())
        
        custom_prebuild = config.get_prebuild()
        
        if not custom_prebuild == None and self.build_file.method_exists(custom_prebuild):
            self.build_file.run_method(custom_prebuild)
        elif self.build_file.prebuild_exists(target_name):
            self.build_file.run_prebuild(target_name)
        
        # Setup
        compiler.set_object_directory(os.path.join(self.pyke_path, target_name))
        
        # Compile
        source_paths = config.get_source_paths();
        source_patterns = config.get_source_patterns();
        
        if source_patterns is None:
            source_patterns = compiler.get_source_patterns()
        
        source_files = self.get_source_files(source_paths, source_patterns)
        object_files = []
        
        for f in source_files:
            object_file = compiler.get_object_file_name(f)
            
            if self.meta_data.has_file_changed(f) or not os.path.exists(object_file):
                print('Compiling %s' % f)
                compiler.compile(f, config.get_compiler_flags())
            else:
                print('%s has not changed, will not compile.' % f)
            
            object_files.append(object_file)
        
        # Link
        output_name = compiler.get_output_name(config.get_output_name())
        output_path = config.get_output_path()
        
        print('Linking %s' % output_name)
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
                    
        compiler.link(os.path.join(output_path, output_name), object_files, config.get_linker_flags())
        
        custom_postbuild = config.get_postbuild()
        
        if not custom_postbuild == None and self.build_file.method_exists(custom_postbuild):
            self.build_file.run_method(custom_postbuild)
        elif self.build_file.postbuild_exists(target_name):
            self.build_file.run_postbuild(target_name)
        
        print('Successfully built %s' % target_name)