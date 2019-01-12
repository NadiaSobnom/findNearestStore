#!usr/bin/python
from setuptools import setup , find_packages
setup (
	name = 'findStore',
	description = 'Find nearest store from a location.',
	version = '0.10',
	packages = find_packages(), # list of all packages
    install_requires = ['inflect'],
    python_requires='>=2.7', # any python greater than 2.7
	test_suite="tests", # where to find tests
	entry_points = {
		'console_scripts': [
			'convert = findStore.__main__:main', # main method
			]
		}
	)
