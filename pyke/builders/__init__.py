from pyke import PykeException

from . import gpp


def factory(compiler, output_type):
	if output_type not in [ 'executable', 'sharedlib', 'dynamiclib' ]:
		raise Exception('Unknown output type: %s' % output_type)
	
	if compiler == 'g++':
		if output_type == 'executable':
			return gpp.ExecutableCompiler()
		elif output_type == 'sharedlib':
			return gpp.SharedLibraryCompiler()
		elif output_type == 'dynamiclib':
			return gpp.DynamicLibraryCompiler()
	
	raise Exception('Unknown compiler: %s' % compiler)

class Factory:
	def __init__(self):
		self._builders = {}
		
		# Load the built-in builders
		self._builders[gpp.NAME] = gpp.factory
	
	def get(self, name, output_type):
		if name not in self._builders:
			raise PykeException('Unknown builder %s.' % name)
		
		factory = self._builders[name]
		builder = factory(output_type)
		
		if builder is None:
			raise PykeException('No builder for %s, %s combo.' % (name, output_type))
		
		return builder