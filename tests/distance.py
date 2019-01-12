from unittest import TestCase
from findStore import constants
import subprocess

class FindDistance(TestCase):

    def run_shell(self, command):
		try:
        	result = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		except Exception as e:
			return e

	def find_nearest_by_address(self):
        inp = '''python findStore/__main__.py --address="1770 Union St, San Francisco, CA 94123"'''  #--output='json' --unit='km'
		out = self.run_shell(inp)
        self.assertEqual(out, constants.address_in_miles + '\n')

	def find_nearest_by_address_in_json(self):
        inp = '''store --address="300 Homer M Adams Pkwy, Alton, IL-62002" --output="json"'''
		out = self.run_shell(inp)
        self.assertEqual(out, constants.address_in_json + '\n')

	def find_nearest_by_address_by_zip(self):
        inp = '''store --zip=94086''' 
		out = self.run_shell(inp)
        self.assertEqual(out, constants.address_from_zip + '\n')

	def find_nearest_by_address_by_zip_km(self):
        inp = '''store --zip=94086''' 
		out = self.run_shell(inp)
        self.assertEqual(out, constants.addess_from_zip_km + '\n')

	def find_nearest_by_address_no_inp_add_zip(self):
        inp = '''store''' 
		out = self.run_shell(inp)
        self.assertEqual(out, constants.no_addr_zip_given + '\n')

