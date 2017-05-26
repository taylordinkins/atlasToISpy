# Parse all types in a specific iSpy JSON file
import json

# Modify filename as required
filename = 'Event_719044414.json'

with open(filename) as data_file:
    data = json.load(data_file)

# Could change Types to Collections or Associations 
for key in data['Types'].keys():
    print key

# Modify subtype for specific key values
subtype = 'Tracks_V3'
for key2 in data['Types'][subtype]:
    print key2

#print 'Collections'
#for key3 in data['Collections']['Tracks_V3']:
#	print key3
