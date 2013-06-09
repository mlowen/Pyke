import pyke

from . import gcc
from . import gpp

class Factory:
	def __init__(self):
		self._builders = {}
		
		# Load the built-in builders
		self._builders[gcc.NAME] = gcc.factory
		self._builders[gpp.NAME] = gpp.factory
	
	def get(self, name, output_type):
		if name not in self._builders:
			raise pyke.PykeException('Unknown builder %s.' % name)
		
		factory = self._builders[name]
		builder = factory(output_type)
		
		if builder is None:
			raise pyke.PykeException('No builder for %s, %s combo.' % (name, output_type))
		
		return builder

	def list(self):
		return [ k for k in self._builders ]