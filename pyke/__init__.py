from . import cli
from . import builders
from . import meta

from .target import TargetWrapper
from .file import File

# Meta Information
__version__ = '0.5.2-beta'
__name__ = 'Pyke'
__description__ = 'A build system for C/C++ using the GCC.'
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
