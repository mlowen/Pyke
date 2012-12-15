from pyke.runners import BaseRunner
from pyke.runners import build
from pyke.runners import clean

class RebuildRunner(BaseRunner):
    def __init__(self, build_file, base_path):
        BaseRunner.__init__(self, build_file, base_path)
        
        self.builder = build.BuildRunner(build_file, self.pyke_path, self.meta_data)
        self.cleaner = clean.CleanRunner(build_file, self.pyke_path, self.meta_data)
        
    def run_target(self, target_name):
        print('Starting rebuild: %s' % target_name)
        
        self.cleaner.run(target_name)
        self.builder.run(target_name)