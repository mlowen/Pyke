from pyke import compilers
from pyke.runners import BaseRunner

class DependencyRunner(BaseRunner):
    def __init__(self, build_file, base_path):
        BaseRunner.__init__(self, build_file, base_path)
    
    def run_target(self, target_name):
        print('Generating file dependencies for %s' % target_name)
        
        if not self.build_file.target_exists(target_name):
            raise Exception('Target %s does not exist.' % target_name)
        
        self.meta_data.set_target(target_name)
        config = self.build_file.run_target(target_name)
        compiler = compilers.factory(config.get_compiler(), config.get_output_type())
        
        source_paths = config.get_source_paths();
        source_patterns = config.get_source_patterns();
        
        if source_patterns is None:
            source_patterns = compiler.get_source_patterns()
        
        source_files = self.get_source_files(source_paths, source_patterns)
        
        for f in source_files:
            self.meta_data.set_file_dependencies(f, compiler.get_file_dependencies(f))
        
        print('Successfully generated file dependencies for %s' % target_name)