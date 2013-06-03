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
		
		if self.target not in self.dependencies:
			self.dependencies[self.target] = { }
	
	# Hashes
	def get_hash_for_file(self, file_name):
		if file_name in self.hashes[self.target]:
			return self.hashes[self.target][file_name]
		
		return None
	
	def set_hash_for_file(self, file_name, hash):
		self.hashes[self.target][file_name] = hash
	
	# Dependencies
	def set_file_dependencies(self, file_name, dependencies):
		if isinstance(dependencies, list):
			data = {}
			
			for d in dependencies:
				data[d] = None
			
			self.dependencies[self.target][file_name] = data
		elif isinstance(dependencies, dict):
			self.dependencies[self.target][file_name] = dependencies
	
	def get_file_dependencies(self, file_name):
		if file_name not in self.dependencies[self.target]:
			return None
		
		return self.dependencies[self.target][file_name].keys()
	
	def get_file_dependency_hash(self, file_name, dependency):
		return self.dependencies[self.target][file_name][dependency]
	
	def set_file_dependency_hash(self, file_name, dependency, hash):
		self.dependencies[self.target][file_name][dependency] = hash
	
	# Other
	def has_file_changed(self, file_name):
		changed = False
		
		# File Hash
		stored_hash = self.get_hash_for_file(file_name)
		computed_hash = md5(open(file_name, 'rb').read()).hexdigest()
		
		if stored_hash is None or stored_hash != computed_hash:
			changed = True
			self.set_hash_for_file(file_name, computed_hash)
		
		# File Dependencies
		dependencies = self.get_file_dependencies(file_name)
		
		if dependencies is not None:
			for dependency in dependencies:
				stored_hash = self.get_file_dependency_hash(file_name, dependency)
				computed_hash = md5(open(dependency, 'rb').read()).hexdigest()
				
				if stored_hash is None or stored_hash != computed_hash:
					changed = True
					self.set_file_dependency_hash(file_name, dependency, computed_hash)
		
		return changed
	
	def delete_target(self, target = None):
		if self.target is None and target is None:
			raise Exception('No target specified')
		
		t = target if target is not None else self.target
		
		if t in self.hashes:
			del self.hashes[t]