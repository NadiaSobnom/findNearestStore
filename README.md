###################### How This Solution Works ##########################

Approach Taken:
1. Imported store.locations.csv to sqlite table named "store". Imported lat, lon in radians
2. Get user cooardinate (latititude, longitude) from zipcode/address by using module geocoder-1.38.1
3. Query the database to get top nearest coordinates from source (step 2). Optimized query by using following:
   a. Calculate fudge factor (Assumption: user is not at the equator)
	   fudge = cos(lat)**2
   b. Query the database store by to get top 5 records ordered by following:
      ((<user-lat> - LAT_COLUMN) * (<user-lat> - LAT_COLUMN) + (<user-lng> - LNG_COLUMN) * (<user-lng> - LNG_COLUMN) * <fudge>)
4. Calculate Haversine distance from user lat, lon to all five nearest locations (setp 4). Return the neares one.

Scipt is written in python.  

How to run the program (cli) on linux:
1. pip install geocoder==1.38.1
2. cd to parent directory findStore
4. Go to findStore/constants.py and Update the path for store-locations.csv (replace path in "data_source" variable). Otherwise import will fail
3. Run 'python findStore/__main__.py --address=<address> --zip=<zipcode> 
   If both zipcode and address given then it'll take address only


Cli commands and outputs:
1. Command: python findStore/__main__.py --zip=94086 --output='json' --units='km'
   Output: {"City": "Sunnyvale", "Store Name": "Sunnyvale", "Distance": "0.201499662676 km", "Zip Code": "94086-6193", "State": "CA", "Longitude": -2.1298658302072044, "Store Location": "SEC S Mathilda Ave & W McKinley Ave", "Address": "298 W McKinley Ave", "Latitude": 0.6522953421284104}
2. Command: python findStore/__main__.py --zip=94086
   Output: Nearest Store: 298 W McKinley Ave, Sunnyvale, CA 94086-6193 
   Distance: 0.125206396831 mi
3. Command: python findStore/__main__.py # No address/zipcode arguments passed
   Output: Please provide one of the following:
    1. Address [ex:--address="1770 Union St, San Francisco, CA 94123"]
	2. Zipcode [ex: --zip=94115]
4. Command: python findStore/__main__.py --zip=94043 --units='kmg' # Invalid units
   Output: Please provide a vaild unit as [--units=(mi|km)]
5. Command: python findStore/__main__.py --zip=94043 --output='random'
   Output: Please provide a vaild outpus as [--output=text|json]
6. Command: python findStore/__main__.py --address="1770 Union St, San Francisco, CA 94123"
   Output: Nearest Store: 2675 Geary Blvd, San Francisco, CA 94118-3400 
   Distance: 1.48465926608 mi

REFERRENCE:
1.  https://en.wikipedia.org/wiki/Haversine_formula
2. https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
3. https://stackoverflow.com/questions/3695224/sqlite-getting-nearest-locations-with-latitude-and-longitude


