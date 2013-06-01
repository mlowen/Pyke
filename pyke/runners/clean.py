import os
import shutil

from pyke import compilers
from pyke.runners import BaseRunner

class CleanRunner(BaseRunner):
    def __init__(self, build_file, base_path, meta_data = None):
        BaseRunner.__init__(self, build_file, base_path, meta_data)
    
    def run_target(self, target_name):
        print('Starting clean: %s' % target_name)
        
        if not self.build_file.target_exists(target_name):
            raise Exception('Target %s does not exist.' % target_name)
        
        # Delete pyke generated  intermediate files
        self.meta_data.delete_target(target_name)
        obj_dir = os.path.join(self.pyke_path, target_name)
        
        if(os.path.exists(obj_dir)):
            shutil.rmtree(obj_dir)
        
        config = self.build_file.run_target(target_name)
        compiler = compilers.factory(config.compiler, config.output_type)
        
        # Check if the build file has a custom clean available.
        if config.clean is not None and self.build_file.method_exists(config.clean):
            self.build_file.run_method(config.clean)
        elif self.build_file.clean_exists(target_name):
            self.build_file.run_clean(target_name)
        else:
            if os.path.exists(config.output_path) and not os.getcwd() == config.output_path:
                shutil.rmtree(config.output_path)
            else:
                output_type = config.output_type
                output_name = compiler.get_output_name(config.output_name)
                
                if os.path.exists(output_name):
                    os.remove(output_name)
                    
        print('Successfully cleaned %s' % target_name)