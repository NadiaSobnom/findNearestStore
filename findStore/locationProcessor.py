import csv
import sqlite3
from geopy import geocoders
from geopy import Nominatim
from math import sin, cos, sqrt, atan2, radians

import sys
import constants

def import_csv_to_db(args):
	"""
	Reads store-locations.csv file and import it's data 
	to newly created mysqlite table named "store"
	"""

	# Reading store-locations.csv
	store_locations = constants.data_source
	try: 
		reader = csv.reader(open(store_locations, 'rU'))
		all_stores = [] # temp csv data storage for db import
		start = False # ignores the Title-row in csv file
		for row in reader:
			if start:
				cur_row = create_tuple(row)
				all_stores.append(cur_row)
			else: 
				start = True

	except Exception as e:
		return e

	# Creating a table named "store" and inserting csv data to it
	conn = sqlite3.connect(constants.store_db)
	try:
		cur = conn.cursor()
		cur.execute(constants.drop_store)
		cur.execute(constants.create_store)
		cur.executemany(constants.insert_to_store, all_stores)
		conn.commit()
		conn.close()

	except Exception as e:
		conn.rollback()
		return e

def find_nearest_store(args):
	"""
	Get nearest 5 locations from database and 
	Returns the address with minimum distance from source
	"""

	# User's source coordinate 
	src_coord = get_source_coordinate(args)
	if type(src_coord) is not list:
		return constants.src_coord_not_found

	# Nearest five stores
	nearest_five = get_nearest_five_stores(src_coord[0], src_coord[1])
	if type(nearest_five) is not dict:
		return constants.no_nearest_store

	# Nearest distance from source 
	nearest_distace = sys.maxsize 
	nearest_address = None
	
	dist = []
	for store in nearest_five:
		dlat = nearest_five[store]['Latitude']
		dlon = nearest_five[store]['Longitude']
		distance = calculate_haversine_distance(radians(src_coord[0]), radians(src_coord[1]), dlat, dlon)
		dist.append(distance)
		if distance < nearest_distace:
			nearest_distace = distance
			nearest_address = nearest_five[store]

		nearest_address['Distance'] = nearest_distace
	return nearest_address



def get_nearest_five_stores(lat, lon):
	"""
	Returns nearest five stores
	Note: Took nearest five to minimize equator error
	"""
	# Stores nearest 5 locations in dictionary
	nearest_five = {} 

	# query that gets nearest five stores
	query = get_nearest_distance_query(lat, lon)
	sql_query = constants.select_nearest.replace(constants.key, query)

	try:
		conn = sqlite3.connect(constants.store_db)
		stores = conn.execute(sql_query)

		for store in stores:
			nearest_five[store[1]] = get_address(store)
		conn.close()

		return nearest_five

	except Exception as e:
		return e

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
	"""
	Calculates Haversine distance between src[lat, lon] to dest[lat, long]
	reference: 
	1. https://en.wikipedia.org/wiki/Haversine_formula
	2. https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
   	"""
	# approx radius of earth in miles
	R = 3969.0

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	return R * c

def get_nearest_distance_query(lat, lon):
	"""
	Will query sqlite store to get top 5 stores sorted by
	below comparator
	Reference: https://stackoverflow.com/questions/3695224/sqlite-getting-nearest-locations-with-latitude-and-longitude
	"""
	# fudge = scaling factor which is 0 at the poles and 1 at the equator
	lat = radians(lat)
	lon = radians(lon)
	fudge = cos(lat)**2
	lat_compataor = '(%f - latitude) * (%f - latitude) + (%f - longitude) * (%f - longitude) * %f' % (lat, lat, lon, lon, fudge)
	return lat_compataor

def get_address(data):
	"""
	Takes sqlite-database-row as input and 
	returns address in a dictionary
	"""
	addr = {} 
	addr["Store Name"] = data[1].encode('UTF8')
	addr["Store Location"] = data[2].encode('UTF8')
	addr["Address"] = data[3].encode('UTF8')
	addr["City"] = data[4].encode('UTF8')
	addr["State"] = data[5].encode('UTF8')
	addr["Zip Code"] = data[6].encode('UTF8')
	addr["Latitude"] = data[7]
	addr["Longitude"] = data[8]

	return addr

def get_coord(data):
	"""
	Takes sqlite-database-row as input and 
	returns coordinate in  a list
	"""
	return [data[7], data[8]]

def get_source_coordinate(args):
	"""
	Find coordinate of a given address or zipcode
	"""
	address = args.address
	zipcode = args.zip

	if address:
		return get_coordinate(address)
	if zipcode:
		return get_coordinate(zipcode)

def get_coordinate(source):
	"""
	Takes a source as user location and return it's coordinates
	"""
	geolocator = Nominatim()
	try:
		coord = geolocator.geocode(source)
		return [coord.latitude, coord.longitude]
	except Exception as e:
		return e
		
def create_tuple(row):
	"""
	Converts a store-locations.csv row to a database insertable-tuple
	"""
	return (unicode(row[0], "utf8"), unicode(row[1], "utf8"), unicode(row[2], "utf8"), unicode(row[3], "utf8"), unicode(row[4], "utf8"), unicode(row[5], "utf8"), radians(float(row[6])), radians(float(row[7])), unicode(row[8], "utf8"))

def convert_miles_to_km(miles):
	return miles * 1.60934

def dict_to_text(dic, unit):
	"""
	Generate human readable text formatted address from a dict
	"""
	return 'Nearest Store: ' + dic['Address'] + ', ' +  dic['City'] + ', ' + dic['State'] + ' ' + dic['Zip Code'] + ' \nDistance: ' + dic['Distance']


	######## ------------------------- TEST --------------------------------

from unittest import TestCase
import subprocess

def ls():
	return run_shell('pwd')

def run_shell(command):
	try:
		result = subprocess.call(command, shell=True)
		return result
	except Exception as e:
		return e

def find_nearest_by_address():
	print "im here"
	inp = '''python findStore/__main__.py --address="1770 Union St, San Francisco, CA 94123"'''
	print inp
	#result = run_shell(inp)
	result = subprocess.call(inp, shell=True)
	print result
	return result
	#out = self.run_shell('ls')
	#self.assertEqual(result, constants.address_in_miles + '\n')

