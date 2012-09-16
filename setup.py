import re

from setuptools import setup

def find_version(file_path):
	matches = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", open(file_path).read(), re.M)
	
	if matches:
		return matches.group(1)
	
	raise RuntimeError("Unable to find version string.")

setup(
	name = 'pyke',
	version = find_version('pyke/__init__.py'),
	description = 'Pyke is a build system for the gcc c++ compiler.',
	long_description = 'Pyke is a build system for the gcc c++ compiler.',
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Build Tools',
		'Environment :: Console',
		'Programming Language :: Python :: 3.2'
	],
	author = 'Mike Lowen',
	author_email = 'mike@mlowen.com',
	url = 'http://mlowen.com',
	license = 'MIT',
	packages = [ 'pyke' ],
	entry_points = { 'console_scripts': [ 'pyke = pyke:main' ]},
	zip_safe = False
)