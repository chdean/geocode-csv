#!/usr/bin/env python
'''
geocode-csv.py - batch geocode a csv file
'''

google_key = ""
csv_delimiter = ","

import csv, sys, geocoder

if len(sys.argv) == 4:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    location_fields_str = sys.argv[3]
else:
    print("Usage: python geocode-csv.py in.csv out.csv addr,city,state")
    sys.exit()

location_fields = location_fields_str.split(',')

def geocode(row):
    """Returns lat/long of a row"""
    attributes = []
    for x in location_fields:
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
fieldnames = list(data[0].keys())
with open(out_file, 'x') as outcsv:
    writer = csv.DictWriter(outcsv, 
                            delimiter = csv_delimiter,
                            fieldnames = fieldnames,
                            extrasaction = 'ignore')
    writer.writeheader()
    for row in data:
        writer.writerow(row)

