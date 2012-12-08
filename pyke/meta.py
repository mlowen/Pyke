import json
import os.path

from hashlib import md5

class MetaFile:
    def __init__(self, path):
        self.file_path = path
        self.hashes = {}
        self.dependencies = {}
        self.target = None
        
        if os.path.exists(self.file_path):
            data = json.load(open(self.file_path))
            
            if 'hashes' in data:
                self.hashes = data['hashes']
            
            if 'dependencies' in data:
                self.dependencies = data['dependencies']
    
    def write(self):
        json.dump({ 'hashes': self.hashes, 'dependencies': self.dependencies }, open(self.file_path, 'w'))
    
    def set_target(self, target):
        self.target = target
        
        if self.target not in self.hashes:
            self.hashes[self.target] = { }
    
    def get_hash_for_file(self, file_name):
        if file_name in self.hashes[self.target]:
            return self.hashes[self.target][file_name]
        
        return None
    
    def set_hash_for_file(self, file_name, hash):
        self.hashes[self.target][file_name] = hash
    
    def has_file_changed(self, file_name):
        stored_hash = self.get_hash_for_file(file_name)
        computed_hash = md5(open(file_name, 'rb').read()).hexdigest()
        
        if stored_hash is not None and stored_hash == computed_hash:
            return False
        
        self.set_hash_for_file(file_name, computed_hash)
        return True
    
    def delete_target(self, target = None):
        if self.target is None and target is None:
            raise Exception('No target specified')
        
        if target is not None:
            del self.hashes[target]
        elif self.target is not None:
            del self.hashes[self.target]