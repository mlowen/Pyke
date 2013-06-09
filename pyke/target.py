import inspect
import os
import pyke
import shutil

from fnmatch import fnmatchcase

_defaults = {
	'source_paths': os.getcwd(),
	'source_patterns': None,
	
	'output_path': os.getcwd(),
	'output_name': os.path.basename(os.getcwd()),
	'output_type': 'executable',
	
	'compiler_flags': [],
	'linker_flags': [],
	
	'is_phoney': False,
	'dependencies': None,
	'builder': None
}

class TargetWrapper:
	def __init__(self, fn):
		self.fn = fn

class Target:
	def __init__(self, name, data, fp):
		self.name = name
		self._file = fp
		self._meta = fp.meta[name]

		self._load_data(_defaults)
		self._load_data(data)

		if not self.is_phoney:
			self._builder = self._file.builders.get(self.builder, self.output_type)
			self._builder.object_directory = os.path.join(self._file.path, self.name)

	def build(self, pending = [], built = []):
		pending.append(self.name)

		if self.dependencies is not None:
			targets = [d for d in self.dependencies if d not in built]
			
			for t in targets:
				if t in pending:
					raise pyke.PykeException('Circular dependency has been detected for target %s.' % t)
				
				built = self._file[t].build(pending, built)

		print('Starting build: %s' % self.name)

		self.prebuild()

		if self.is_phoney and self.run is not None:
			self.run()
		elif not self.is_phoney:			
			# Compile
			object_files = self._compile()
			
			# Link
			self._link(object_files)

		self.postbuild()

		built.append(self.name)
		pending = [t for t in pending if t != self.name]
		
		print('Successfully built %s' % self.name)

		return built

	def clean(self):
		if self.is_phoney:
			return

		print('Starting clean: %s' % self.name)
		
		# Delete pyke generated  intermediate files
		self._meta.clean()

		if self._builder is not None and os.path.exists(self._builder.object_directory):
			shutil.rmtree(self._builder.object_directory)

		clean_name = 'clean_%s' % self.name

		if any(clean_name == m and inspect.isroutine(m) for m in inspect.getmembers(self._file.module)):
			method = getattr(self._file.module, clean_name)
			method()
		else:
			if os.path.exists(self.output_path) and not os.getcwd() == self.output_path:
				shutil.rmtree(self.output_path)
			else:
				output_type = self.output_type
				output_name = self._builder.output_name(self.output_name)
				
				if os.path.exists(output_name):
					os.remove(output_name)
		
		print('Successfully cleaned %s' % self.name)

	def rebuild(self):
		self.clean()
		self.build()

	def prebuild(self):
		name = 'pre_%s' % self.name

		if any(name == m and inspect.isroutine(m) for m in inspect.getmembers(self._file.module)):
			method = getattr(self._file.module, name)
			method()

	def postbuild(self):
		name = 'post_%s' % self.name
		
		if any(name == m and inspect.isroutine(m) for m in inspect.getmembers(self._file.module)):
			method = getattr(self._file.module, name)
			method()

	def generate_dependencies(self):
		print('Generating file dependencies for %s' % self.name)

		for f in self.get_source_files():
			self._meta[f].set_dependencies(self._builder.dependencies(f))
		
		print('Successfully generated file dependencies for %s' % self.name)

	def get_source_files(self):
		patterns = self.source_patterns
		
		if patterns is None:
			patterns = self._builder.patterns

		source_files = []

		for path in self.source_paths:
			for root, directories, files in os.walk(path):
				source_files += [os.path.join(root, f) for f in files if any(fnmatchcase(f, p) for p in patterns)]

		return source_files

	# Private methods

	def _compile(self):
		object_files = []
		source_files = self.get_source_files()

		for f in source_files:
			object_file = self._builder.object_file_name(f)
			
			if self._meta[f].changed() or not os.path.exists(object_file):
				print('Compiling %s' % f)
				self._builder.compile(f, self.compiler_flags)
			else:
				print('%s has not changed, will not compile.' % f)
			
			object_files.append(object_file)
		
		self._meta.tidyup(source_files)

		return object_files

	def _link(self, object_files):
		output_name = self._builder.output_name(self.output_name)
		
		print('Linking %s' % output_name)
		
		if not os.path.exists(self.output_path):
			os.makedirs(self.output_path)
					
		self._builder.link(os.path.join(self.output_path, output_name), object_files, self.linker_flags)

	def _load_data(self, data):
		for key in data:
			self.__dict__[key] = data[key]
