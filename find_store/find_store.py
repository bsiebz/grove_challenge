#! /usr/bin/python
"""
Find Store
  find_store will locate the nearest store (as the crow flies) from
  store-locations.csv, print the matching store address, as well as
  the distance to that store.

Usage:
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>           Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address="<address>" Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)       Display units in miles or kilometers [default: mi]
  --output=(text|json)  Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
"""

from docopt import docopt
from uszipcode import SearchEngine
from geopy.geocoders import Nominatim
import math, sys, json, pandas as pd, os

def main():
    pd.options.mode.chained_assignment = None
    arguments = docopt(__doc__, version='Find Store 1.0')
    address = arguments['--address']
    zipcode = arguments['--zip']
    geoService = GeoService()
    
    if geoService.validAddressOrZip(address):
      cur_lat_long = geoService.geo_address_search(address)
      geoService.main_helper(arguments,cur_lat_long)
    elif geoService.validAddressOrZip(zipcode):
      cur_lat_long = geoService.geo_zip_search(zipcode)
      geoService.main_helper(arguments,cur_lat_long)
    else:
      print("Please input a valid zip or address.")
    
    
class GeoService:    
  def validAddressOrZip(self,str):
    return bool(str is not None and str.strip().replace("=",""))
  
  def main_helper(self,arguments, cur_lat_long):
    units = arguments['--units']
    output = arguments['--output']
    
    store_locations = pd.read_csv(os.path.abspath("find_store/store-locations.csv"))
    min_dist_km = sys.maxint
    min_row =[]
    
    length = len(store_locations)
    for index in range(0, length):
      store_info = store_locations.iloc[index]
      cur_dist_km = self.geo_distance_formula(store_info, cur_lat_long)
      if cur_dist_km < min_dist_km:
        min_row = store_info
        min_dist_km=cur_dist_km
    
    if units.lower() == "km":
      min_dist = min_dist_km
    elif units.lower() =="mi":
      min_dist = min_dist_km*0.621371
    else:
      print("...defaulting units to miles.")
      units = "mi"
      min_dist = min_dist_km*0.621371
      
    if output == "json":
      json_row = min_row
      json_row.loc["units"] = units
      json_row.loc["distance"]= min_dist
      print(json_row.to_json())
    else:
      txt_string = str("Closest store found:\nDistance ("+units+"): \t"+str(min_dist)+"\n"+str(min_row))
      print(txt_string)
     
     
  #Pass in Zip get lat/long
  def geo_zip_search(self,zipcode):
    search = SearchEngine(simple_zipcode=True)
    zipcode = search.by_zipcode(zipcode)
    zip_dict = zipcode.to_dict()
    return (zip_dict['lat'],zip_dict['lng'])
    
    
  #Pass in Address get lat/long 
  def geo_address_search(self,address):
    geolocator = Nominatim(user_agent="Bryan")
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)
  
  
  #Pass in row of Store info, location with lat/long, and units to return
  def geo_distance_formula(self,store_info, location):
    #implementation of haversine formula
    lat1,lon1=location
    lat2=store_info.loc["Latitude"]
    lon2=store_info["Longitude"]
          
    earth_radius=6371 #radius in km
    phi_1=math.radians(lat1)
    phi_2=math.radians(lat2)
  
    delta_phi=math.radians(lat2-lat1)
    delta_lambda=math.radians(lon2-lon1)
  
    a=math.sin(delta_phi/2.0)**2+math.cos(phi_1)*math.cos(phi_2)*math.sin(delta_lambda/2.0)**2
    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    return earth_radius*c  
    
  
if __name__ == "__main__":
    main()