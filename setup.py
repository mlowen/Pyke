import re
import pyke

from setuptools import setup

setup(
	name = pyke.__name__,
	version = pyke.__version__,
	description = pyke.__description__,
	long_description = pyke.__description__,
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Build Tools',
		'Environment :: Console',
		'Programming Language :: C++',
		'Programming Language :: Python :: 3'
	],
	author = pyke.__author__,
	author_email = pyke.__author_email__,
	url = pyke.__homepage__,
	license = pyke.__license__,
	packages = [ 'pyke', 'pyke.compilers', 'pyke.runners' ],
	entry_points = { 'console_scripts': [ 'pyke = pyke:main' ]},
	zip_safe = False
)