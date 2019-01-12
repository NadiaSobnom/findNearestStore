"""
This file contains the contants
"""
# Constants

# This has to be changed to the path where user has store-locations.csv 
data_source = "/home/nadia/codingChallenge/geoLocator/locations/store-locations.csv"
key = '<KEY>'
uname = "nsobnom"
store_db = "store.sl3"
units = ['km', 'mi']
output = ['json', 'text']

# SQLite query
drop_store = "DROP TABLE IF EXISTS store;"
create_store = "CREATE TABLE store (id INTEGER PRIMARY KEY, name TEXT, location TEXT, address TEXT, city TEXT, state TEXT, zipcode TEXT, latitude REAL, longitude REAL, county TEXT);"
insert_to_store = "INSERT INTO store (name, location, address, city, state, zipcode, latitude, longitude, county) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
select_nearest = "SELECT * FROM store ORDER BY <KEY> LIMIT 5" 

# Error messages
import_failed = "Failed to imporst csv to sqlite database. Details: "
no_zip_addr_given = '''Please provide one of the following:\n 1. Address [ex:--address="1770 Union St, San Francisco, CA 94123"]\n 2. Zipcode [ex: --zip=94115]'''
src_coord_not_found = "Failed to find the latitude-longitude for your location. Please make sure you provided correct address or zipcode."
invaild_unit = "Please provide a vaild unit as [--units=(mi|km)]"
invaild_output = "Please provide a vaild outpus as [--output=text|json]"
no_nearest_store = "Failed to find top nearest five stores"

# Expected output for test cases
address_in_miles = "Nearest Store: 2675 Geary Blvd, San Francisco, CA 94118-3400 \nDistance: 1.48465926608 mi"
address_from_zip = "Nearest Store: 298 W McKinley Ave, Sunnyvale, CA 94086-6193 \nDistance: 1.2506068009 mi"
addess_from_zip_km = "Nearest Store: 555 Showers Dr, Mountain View, CA 94040-1432 \nDistance: 1.54843198408 km"
address_in_json = '''{"City": "Alton", "Store Name": "Alton", "Distance": "0.175479573466 mi", "Zip Code": "62002-5928", "State": "IL", "Longitude": -1.573768498592666, "Store Location": "NEC Homer Adams Pkwy & Alby Rd", "Address": "300 Homer M Adams Pkwy", "Latitude": 0.6793119777890975}'''
no_addr_zip_given = '''Please provide one of the following:\n1. Address [ex:--address="1770 Union St, San Francisco, CA 94123"]\n2. Zipcode [ex: --zip=94115]'''

