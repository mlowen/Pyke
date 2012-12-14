import os
import shutil

from pyke import compilers
from pyke.runners import BaseRunner

class CleanRunner(BaseRunner):
    def __init__(self, build_file, base_path):
        BaseRunner.__init__(self, build_file, base_path)
    
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
        compiler = compilers.factory(config.get_compiler(), config.get_output_type())
        custom_clean = config.get_clean()
        
        # Check if the build file has a custom clean available.
        if custom_clean is not None and self.build_file.method_exists(custom_clean):
            self.build_file.run_method(custom_clean)
        elif self.build_file.clean_exists(target_name):
            self.build_file.run_clean(target_name)
        else:
            output_path = config.get_output_path()
            
            if os.path.exists(output_path) and not os.getcwd() == output_path:
                shutil.rmtree(output_path)
            else:
                output_type = config.get_output_type()
                output_name = compiler.get_output_name(config.get_output_name())
                
                if os.path.exists(output_name):
                    os.remove(output_name)
                    
        print('Successfully cleaned %s' % target_name)