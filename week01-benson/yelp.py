import urllib.request
import requests
import csv

# secrets.py is ignored by git
from secrets import yelp_auth_token

def fetch_data_and_write_csv(station_coordinates):
    headers = {"Authorization": yelp_auth_token }
    base_url = 'https://api.yelp.com/v3/businesses/search'
    businesses = []
    # quarter mile in meters
    search_radius = int(0.25 / 0.00062137)
    endpoint = lambda lt, lg: '{0}?latitude={1}&longitude={2}&radius={3}&limit=50'.format(base_url, lt, lg, search_radius)

    for sc in station_coordinates:
        station, latitude, longitude = sc
        yelp_data = requests.get(endpoint(latitude, longitude), headers=headers).json()
        for business in yelp_data['businesses']:
            businesses.append({
                'name': business.get('name', ''),
                'price': business.get('price', ''),
                'rating': business.get('rating', ''),
                'latitude': business.get('latitude', ''),
                'longitude': business.get('longitude', ''),
                'station': station,
                'distance': business.get('distance', '')
            })

    with open('yelp_data.csv', 'w') as yelp_data_csv:
        dict_writer = csv.DictWriter(yelp_data_csv, businesses[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(businesses)

station_coordinates = [
    ['34 ST-PENN STA', 40.750373, -73.991057],
    ['GRD CNTRL-42 ST', 40.751776, -73.976848],
    ['34 ST-HERALD SQ', 40.749719, -73.987823],
    ['23 ST', 40.744081, -73.995657],
    ['42 ST-PORT AUTH', 40.757308, -73.989735],
    ['59 ST', 40.762526, -73.967967],
    ['TIMES SQ-42 ST', 40.755290, -73.987495],
    ['14 ST-UNION SQ', 40.734673, -73.989951],
    ['FULTON ST', 40.709416, -74.006571],
    ['BEDFORD PK BLVD', 40.689627, -73.953522],
    ['BEDFORD PK BLVD', 40.873244, -73.887138],
    ['BEDFORD PK BLVD', 40.873412, -73.890064]
]

fetch_data_and_write_csv(station_coordinates)
