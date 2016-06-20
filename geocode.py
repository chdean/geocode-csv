#!/usr/bin/env python
'''
geocode.py - batch geocode a csv file
'''


google_key = "" # TODO
csv_delimiter = ";"

import csv, sys, geocoder

if len(sys.argv) == 4:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    fieldnames_str = sys.argv[3]
else:
    print("Usage: python geocode.py in.csv out.csv addr,city,state")
    sys.exit()

fieldnames = fieldnames_str.split(',')

def geocode(row):
    """Returns lat/long of a row"""
    attributes = []
    for x in fieldnames:
        attributes.append(row[x])
    full_address = ', '.join(attributes)
    
    print("Geocoding:", full_address)
    
    g = geocoder.google(full_address, key = google_key)

    if g.latlng:
        print(str(g.latlng))
    else:
        print("Failed")
    return g.latlng

data = []
with open(in_file) as csvfile:
    reader = csv.DictReader(csvfile, delimiter = csv_delimiter)
    for row in reader:
        data.append(row)
for record in data:
    latlng = geocode(record)
    if latlng:
        record['Latitude'] = str(latlng[0])
        record['Longitude'] = str(latlng[1])
    else:
        record['Latitude'] = ''
        record['Longitude'] = ''

# TODO - write to new csv file
