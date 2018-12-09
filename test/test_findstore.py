#! /usr/bin/python
import pytest, os, pandas as pd
from find_store import *

def test_valid_address():
    bad_address = GeoService().validAddressOrZip("=")
    assert bad_address is False
    
def test_geo_zip_search():
    lat_lon_tuple = GeoService().geo_zip_search("94109")
    assert lat_lon_tuple[0] is not None
    assert lat_lon_tuple[1] is not None
    
def test_geo_address_search():
    address = "1770 Union St, San Francisco, CA 94123"
    lat,lon = GeoService().geo_address_search(address)
    assert lat is not None
    assert lon is not None
    
def test_geo_distance_formula():
    location = (37.79, -122.42)
    store_locations = pd.read_csv(os.path.abspath("find_store/store-locations.csv"))
    distance = GeoService().geo_distance_formula(store_locations.iloc[0],location)
    assert (distance >= 2537) #2537.6170265 is expected distance