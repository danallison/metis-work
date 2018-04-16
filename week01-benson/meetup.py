import urllib.request
import requests
import csv
from math import radians, cos, sin, asin, sqrt

# secrets.py is ignored by git
from secrets import meetup_auth_token

# Copied from https://stackoverflow.com/a/15737218
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def fetch_data_and_write_csv(station_coordinates):
    headers = {"Authorization": meetup_auth_token }
    base_url = 'https://api.meetup.com/find/upcoming_events'
    events = []
    # one mile is the minimum radius the API will accept
    search_radius = 1
    search_query = 'women'
    endpoint = lambda lt, lg: '{0}?lat={1}&lon={2}&radius={3}&text={4}&key={5}'.format(base_url, lt, lg, search_radius, search_query, meetup_auth_token)

    for sc in station_coordinates:
        station, latitude, longitude = sc
        meetup_data = requests.get(endpoint(latitude, longitude), headers=headers).json()
        print(meetup_data)
        for event in meetup_data['events']:
            lat = event.get('venue', {}).get('lat', '')
            lon = event.get('venue', {}).get('lon', '')
            if lat and lon:
                distance = haversine(longitude, latitude, lon, lat)
                # Convert km to miles
                distance *= 0.62137
            else:
                continue
            events.append({
                'group_name': event.get('group', {}).get('name', ''),
                'yes_rsvp_count': event.get('yes_rsvp_count', ''),
                'latitude': lat,
                'longitude': lon,
                'station': station,
                'distance': distance,
                'proximity_weighted_rsvp_count': event.get('yes_rsvp_count', 0) * (1 - distance)
            })

    with open('meetup_data.csv', 'w') as meetup_data_csv:
        dict_writer = csv.DictWriter(meetup_data_csv, events[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(events)

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
