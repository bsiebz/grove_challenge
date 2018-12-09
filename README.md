README.md

Hi, just wanted to start by saying thanks for the opportunity to do this coding challenge.
To be honest it has been a bit since I've used python, but I wanted to use this opportunity
to brush back up and learn some more skills that would be useful for the future, hopefully
for both parties. 

This solution follows the haversine formula, when calculating the distance between two points
we gather the latitude and longitude pairs initially. Since the input can be in a zipcode or a
full string address. I decided to use SearchEngine from uszipcode to turn the zipcode into
a tuple pair, and Nominatim from geopy.geocoders to get the tuple pair from the address. Once
we have both tuple pairs, we call the geo_distance_formula which implements haversine. This
is calculated initially in KM and converted to miles if either no "output" argument is supplied
or if "mi"/"MI" is provided.

An assumption made was the the addresses and zipcodes (like the data presented in the csv),
would all be internal to the US. Also, if output is json or txt (default) this formatting is
printed to the console (if customer desired for an output file to be .txt or .json this could
be changed). 



References:
python docs
https://docs.pytest.org/en/latest/
https://nathanrooy.github.io/posts/2016-09-07/haversine-with-python/
