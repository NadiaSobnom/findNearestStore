import argparse
import logging
import json

import locationProcessor
import constants

def cli():
    parser = argparse.ArgumentParser(description="Finding nearest store location...") # App description

    parser.add_argument("-z", "--zip", type=int, help="Nearest store to this zip code")
    parser.add_argument("-u", "--units", help="Please provide preferred units as [--units=(mi|km)]", type=str, default='mi')
    parser.add_argument("-a", "--address", type=str, help="Nearest store to this address.")
    parser.add_argument("-o", "--output", help="Acceptable output format [--output=text|json]", type=str, default="text")

    return parser.parse_args()

def main():
	args = cli() # get user inputs from command line
	zipcode = args.zip
	address = args.address

	# Validating arguments
	if not address and not zipcode:
		print constants.no_zip_addr_given
		return
		
	units = args.units
	if units.lower() not in constants.units:
		print constants.invaild_unit
		return
		
	output = args.output
	if output.lower() not in constants.output:
		print constants.invaild_output
		return

	# Importing csv to sqlite
	# **** Onetime import is enough. Below 4 lines can be commented after one run (after creating the sqlite db) ***** 
	import_res = locationProcessor.import_csv_to_db(args)
	if type(import_res) is str: # import returned exception
		print constants.import_failed + import_res
		return

	# Find nearest store and it's distance
	nearest_store = locationProcessor.find_nearest_store(args)

	# Nearest store stored in a dict
	if type(nearest_store) is dict: # Nearest store found successfully
		store_distance = nearest_store['Distance'] # in miles
		nearest_store['Distance'] = str(store_distance) + ' ' + units

		if units == constants.units[0]: # unit is km 	
			distance_km = locationProcessor.convert_miles_to_km(store_distance)
			nearest_store['Distance'] = str(distance_km) + ' ' + units

		if output == constants.output[0]: # output json
			print json.dumps(nearest_store) 	
			return

		else: # output text	
			store_address = locationProcessor.dict_to_text(nearest_store,  units)
			print store_address
			return

	# Any exception happend for which result was not found
	print nearest_store 

if __name__ == '__main__':
	main()
