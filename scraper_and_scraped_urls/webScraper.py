import requests
import os
from bs4 import BeautifulSoup
import re
import time
from urllib.request import urlopen
import math
from geopy.geocoders import Nominatim
from collections import defaultdict
import json

geolocator = Nominatim(user_agent='chadlei')
# Example use:
# city = 'San Francisco, united states of america'
# latitude,longitude = geolocator.geocode(city).latitude,geolocator.geocode(city).longitude

cities_to_search = ['irvine', 'los angeles', 'san francisco', 'new york']
keywords = ['software', 'developer', 'full', 'back', 'front', 'ios', 'mobile']
negative_keywords = ['senior', 'sr', 'staff']

# Reads a file and returns a list of all urls
def url_reader(file_name):
    with open(file_name, 'r') as filetoread:
        urls = filetoread.readlines()
    return urls

# Reads a json file and returns a default dict
def create_dict(file_name,default_type):
    with open(file_name) as f:
           dict = json.load(f)
           dict = defaultdict(default_type,dict)
    return dict

# Updates json file on newly added values
def update_dict_file(file_name, dict_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(dict_name, f, ensure_ascii=False, indent=4, sort_keys=True)

# Function to Calculate Distance https://stackoverflow.com/questions/10693699/calculate-distance-between-cities-find-surrounding-cities-based-on-geopt-in-p
def HaversineDistance(location1, location2):
    """Method to calculate Distance between two sets of Lat/Lon."""
    lat1, lon1 = location1
    lat2, lon2 = location2
    earth = 6371 #Earth's Radius in Kms.
    earth_in_miles = 3959 #radius in miles
    #Calculate Distance based in Haversine Formula
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = earth_in_miles * c
    return d
# print(HaversineDistance((latitude,longitude), (latitude,longitude)))

# If latitudes and longitudes have not been calculated already, then calculate and store it
def get_dict_value(dict,city):
    if (dict[city] == ()):
        city_geo = geolocator.geocode(city + ', united states of america') # Geocode library requires USA to clarify search
        dict[city] = (city_geo.latitude,city_geo.longitude)

# Scrapes the given webpage for any open positions that match search criteria
def web_scraper(location_distances,lats_longs,urls):
    for url in urls:
        try:
            html_page = urlopen(url.strip('\n'))
            soup = BeautifulSoup(html_page, "html.parser")
            jobs_found = set()
            for div in soup.find_all('div', {'class':"opening"}):
                # Find's the location of the current job opening
                for location in div.find_all('span'):
                    # Checks if there are multiple locations for the position
                    if ('and' in location.string):
                        input = location.string.lower().split(' and ')[0]
                    else:
                        input = location.string.lower().split(',')[0]
                    # If location is remote, automatically add link and apply
                    if ('remote' in location.string.lower() or 'anywhere' in location.string.lower()):
                        # Checks if job title matches what I'm seeking
                        if link.string != None and any(kw in link.string.lower() for kw in keywords) and not any(kw in (link.string).lower() for kw in negative_keywords):
                            jobs_found.add('https://boards.greenhouse.io' + str(link.get('href')) + '\n')
                    # If not, then check if the job's location is in the area I want to work for
                    else:
                        distances = []
                        get_dict_value(lats_longs,input)
                        latitude,longitude = lats_longs[input]
                        # Calculate the distance from each job's location to the area I want to work in
                        for city in cities_to_search:
                            get_dict_value(lats_longs,city)
                            latitude2,longitude2 = lats_longs[city]
                             # If the distance has not been calculated already, then calculate it
                            if (location_distances[input+'-'+city] == 0):
                                haversine_distance = HaversineDistance((latitude,longitude), (latitude2,longitude2))
                                location_distances[input+'-'+city] = haversine_distance + 1
                            distances.append( (input, city, location_distances[input+'-'+city]) )
                        # If the job's location is near any of my desired locations, then add it so I can apply
                        if any(distance <= 40 for input,city,distance in distances):
                            for link in div.find_all('a'):
                                if link.string != None and any(kw in link.string.lower() for kw in keywords) and not any(kw in (link.string).lower() for kw in negative_keywords):
                                    jobs_found.add('https://boards.greenhouse.io' + str(link.get('href')) + '\n')
        except:
            # Error means that the job's location is not located in the US or url doesn't exist, so you can choose how to continue
            print(url.split('.io/')[1].strip('/\n').capitalize() + ' - ' + 'Error finding jobs')
            continue
        if len(jobs_found) == 0:
            print(url.split('.io/')[1].strip('/\n').capitalize() + ' - ' + 'No jobs were found')
        else:
            with open('scraped_jobs.txt', 'a') as filetowrite:
                filetowrite.writelines(list(jobs_found))
            update_dict_file('location_distances.json', location_distances)
            update_dict_file('latitude_longitude.json', lats_longs)
            print(url.split('.io/')[1].strip('/\n').capitalize() + ' - ' + str(len(jobs_found)) + ' job(s) found')






if __name__ == '__main__':
    # start_time = time.time() # Timer for how long the program takes
    # Imports previously calculated distances
    location_distances = create_dict('location_distances.json',int)
    # Imports previously calculated latitudes and longitudes
    lats_longs = create_dict('latitude_longitude.json',tuple)
    # Imports all websites needed to scrap
    urls = url_reader('job_websites_to_scrap.txt')
    web_scraper(location_distances,lats_longs,urls)
    print('\nJob Scraping Complete!')
    # print("--- %s seconds ---" % (time.time() - start_time))
