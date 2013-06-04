from . import cli
from . import compilers
from . import meta

from .target import TargetWrapper
from .file import File

# Meta Information
__version__ = '0.5.1-beta'
__name__ = 'Pyke'
__description__ = 'Build system for the GCC C++ compiler.'
__author__ = 'Mike Lowen'
__author_email__ = 'mike@mlowen.com'
__homepage__ = 'http://mlowen.com'
__license__ = 'MIT'

# Constants

DEFAULT_TARGET = 'default'
DEFAULT_FILE_NAME = 'build.pyke'

class PykeException(BaseException):
	def __init__(self, message):
		BaseException.__init__(self, message)

		self.message = message

def target(fn):
	return TargetWrapper(fn)
