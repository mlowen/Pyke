import json
import os.path

from hashlib import md5

class TargetFile:
	def __init__(self, path, data = None):
		self.path = path
		self.hash = None
		self.dependencies = {}

		if data is not None:
			self.hash = data['hash']
			self.dependencies = data['dependencies']

	def raw(self):
		return {
			'hash': self.hash,
			'dependencies': self.dependencies
		}

	def clean(self):
		self.hash = None

		for dependency in self.dependencies:
			self.dependencies[dependency] = None

	def changed(self):
		changed = False
		
		# File Hash
		computed_hash = md5(open(self.path, 'rb').read()).hexdigest()
		
		if self.hash is None or self.hash != computed_hash:
			changed = True
			self.hash = computed_hash
		
		# File Dependencies
		for dependency in self.dependencies:
			stored_hash = self.dependencies[dependency]
			computed_hash = md5(open(dependency, 'rb').read()).hexdigest()
			
			if stored_hash is None or stored_hash != computed_hash:
				changed = True
				self.dependencies[dependency] = computed_hash
		
		return changed

	def set_dependencies(self, dependencies):
		for d in dependencies:
			self.dependencies[d] = None

class Target(dict):
	def __init__(self, fp, data = {}):
		dict.__init__(self)
		self._file = fp

		for f in data:
			self[f] = TargetFile(f, data[f])

	def raw(self):
		data = {}

		for f in self:
			data[f] = self[f].raw()

		return data

	def clean(self):
		for f in self:
			self[f].clean()

	def __getitem__(self, key):
		if key not in self:
			self[key] = TargetFile(key)

		return dict.__getitem__(self, key)

class File(dict):
	def __init__(self, path):
		dict.__init__(self)

		self._path = path

		if os.path.exists(self._path):
			data = json.load(open(self._path))

			if isinstance(data, dict):
				for t in data: self[t] = Target(self, data[t])

	def write(self):
		data = {}

		for t in self:
			data[t] = self[t].raw()

		json.dump(data, open(self._path, 'w'))

	def __getitem__(self, key):
		if key not in self:
			self[key] = Target(self)

		return dict.__getitem__(self, key)
