import inspect
import os
import pyke
import shutil

from fnmatch import fnmatchcase
from pyke import compilers

_defaults = {
	'source_paths': os.getcwd(),
	'source_patterns': None,
	
	'output_path': os.getcwd(),
	'output_name': os.path.basename(os.getcwd()),
	'output_type': 'executable',
	
	'compiler_flags': [],
	'linker_flags': [],
	
	'prebuild': None,
	'postbuild': None,
	'clean': None,
	
	'is_phoney': False,
	'dependencies': None
}

class TargetWrapper:
	def __init__(self, fn):
		self.fn = fn

class Data:
	def __init__(self, data = None):
		self._load_data(_defaults)
		self._load_data(data)
	
	def _load_data(self, data):
		for key in data:
			self.__dict__[key] = data[key]

class Target:
	def __init__(self, name, data, fp):
		self.name = name
		self._file = fp		
		self._data = Data(data)

	def build(self, pending = [], built = []):
		pending.append(self.name)

		if self._data.dependencies is not None:
			targets = [d for d in self._data.dependencies if d not in built]
			
			for t in targets:
				if t in pending:
					raise pyke.PykeException('Circular dependency has been detected for target %s.' % t)
				
				built = self._file[t].build(pending, built)

		print('Starting build: %s' % self.name)

		self._file.meta_data.set_target(self.name)
		self.prebuild()

		if self._data.is_phoney and self._data.run is not None:
			self._data.run()
		elif not self._data.is_phoney:
			# Setup
			compiler = compilers.factory(self._data.compiler, self._data.output_type)
			compiler.set_object_directory(os.path.join(self._file.path, self.name))
			
			# Compile
			object_files = self._compile(compiler)
			
			# Link
			self._link(compiler, object_files)

		self.postbuild()

		built.append(self.name)
		pending = [t for t in pending if t != self.name]
		
		print('Successfully built %s' % self.name)

		return built

	def clean(self):
		print('Starting clean: %s' % self.name)
				
		# Delete pyke generated  intermediate files
		self._file.meta_data.delete_target(self.name)
		obj_dir = os.path.join(self._file.path, self.name)
		
		if(os.path.exists(obj_dir)):
			shutil.rmtree(obj_dir)

		compiler = compilers.factory(self._data.compiler, self._data.output_type)
		clean_name = 'clean_%s' % self.name

		# Check if the build file has a custom clean available.
		if self._data.clean is not None:
			self._data.clean()
		elif any(clean_name == m and inspect.isroutine(m) for m in inspect.getmembers(self._file.module)):
			method = getattr(self._file.module, clean_name)
			method()
		else:
			if os.path.exists(self._data.output_path) and not os.getcwd() == self._data.output_path:
				shutil.rmtree(self._data.output_path)
			else:
				output_type = self._data.output_type
				output_name = compiler.get_output_name(self._data.output_name)
				
				if os.path.exists(output_name):
					os.remove(output_name)
					
		print('Successfully cleaned %s' % self.name)

	def rebuild(self):
		self.clean()
		self.build()

	def prebuild(self):
		if self._data.prebuild is not None:
			self._data.prebuild()
		else:
			name = 'pre_%s' % self.name

			if any(name == m and inspect.isroutine(m) for m in inspect.getmembers(self._file.module)):
				method = getattr(self._file.module, name)
				method()

	def postbuild(self):
		if self._data.postbuild is not None:
			self._data.postbuild()
		else:
			name = 'post_%s' % self.name
			
			if any(name == m and inspect.isroutine(m) for m in inspect.getmembers(self._file.module)):
				method = getattr(self._file.module, name)
				method()

	def generate_dependencies(self):
		print('Generating file dependencies for %s' % self.name)
		
		self._file.meta_data.set_target(self.name)
		compiler = compilers.factory(self._data.compiler, self._data.output_type)
		
		source_paths = self._data.source_paths
		source_patterns = self._data.source_patterns
		
		if source_patterns is None:
			source_patterns = compiler.get_source_patterns()
		
		source_files = self._get_source_files(source_paths, source_patterns)
		
		for f in source_files:
			self._file.meta_data.set_file_dependencies(f, compiler.get_file_dependencies(f))
		
		print('Successfully generated file dependencies for %s' % self.name)

	# Private methods

	def _compile(self, compiler):
		source_patterns = self._data.source_patterns
		
		if source_patterns is None:
			source_patterns = compiler.get_source_patterns()
		
		source_files = self._get_source_files(self._data.source_paths, source_patterns)
		object_files = []
		
		for f in source_files:
			object_file = compiler.get_object_file_name(f)
			
			if self._file.meta_data.has_file_changed(f) or not os.path.exists(object_file):
				print('Compiling %s' % f)
				compiler.compile(f, self._data.compiler_flags)
			else:
				print('%s has not changed, will not compile.' % f)
			
			object_files.append(object_file)
		
		return object_files

	def _link(self, compiler, object_files):
		output_name = compiler.get_output_name(self._data.output_name)
		
		print('Linking %s' % output_name)
		
		if not os.path.exists(self._data.output_path):
			os.makedirs(self._data.output_path)
					
		compiler.link(os.path.join(self._data.output_path, output_name), object_files, self._data.linker_flags)

	def _get_source_files(self, paths, patterns):
		source_files = []

		for path in paths:
			for root, directories, files in os.walk(path):
				source_files += [os.path.join(root, f) for f in files if any(fnmatchcase(f, p) for p in patterns)]

		return source_files
