# Parse through a specific JSON file in proper iSpy format
import json

# Modify filename as required
filename = 'Event_719044414.json'

with open(filename) as data_file:
    data = json.load(data_file)

for key in data.keys():
    print key
    print 'KEY2'
    for key2 in data[key]:
        print key2

