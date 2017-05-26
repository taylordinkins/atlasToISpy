# Collect and convert Tracks from JiveXML data to iSpy JSON format
# Run this file, then run copyJson.py if desired to copy files to iSpy directory location
# Taylor Dinkins

import json, io, collections as coll
from xml.dom import minidom
import math, glob, os

# Globals for ease of access
atlasTrackIndex = 0
atlasPointIndex = 1
thetaVals = []
numPolyLines = []

def convertEta(data):
	retVal = []
	for elem in data:
		theta = (math.pi/2) - math.atan(float(elem))
		thetaVals.append(theta)
		retVal.append(-math.log(math.tan(theta/2)))
	return retVal

#change points to just be one fucking big list
#not list of lists
def getPoints(xPoints, yPoints, zPoints):
	retVal = []
	for i in range(len(xPoints)):
		currentX = float(xPoints[i])
		currentY = float(yPoints[i])
		currentZ = float(zPoints[i])
		point = [currentX/100, currentY/100, currentZ/100]
		retVal.append([point])
	return retVal		

def createAssociations(numPolyLines):
	retVal = []
	count = 0
	pointsIndex = 0
	for i in range(len(numPolyLines)):
		for j in range(int(numPolyLines[i])):
			trackNum = [atlasTrackIndex, i]
			pointNum = [atlasPointIndex, count]
			toAdd = [trackNum, pointNum]
			retVal.append(toAdd)
			count+=1
	return retVal

# Collect all data from XML
def collectTracks(itemlist):
	#Collections variables
	collections = []
	retData = []
	pt = []
	phi = []
	eta = []
	xPoints = []
	yPoints = []
	zPoints = []
	pointsCollection = []
	associations = []
	# Charge, rp, and caloEnergy are just placeholders currently
	charge = 1
	rp = [0, 0, 0]
	caloEnergy = 0
	# itemlist is all Tracks tags
	# iterate over all looking for CombinedInDetTracks key
	# collect all necessary data from children
	for s in itemlist:
		if s.attributes['storeGateKey'].value == 'CombinedInDetTracks':
			count = 0
			for r in s.childNodes:
				if (count % 2) != 0:
					if r.nodeName == 'pt':
						pt = r.firstChild.data.decode("utf-8").split()
					elif r.nodeName == 'phi0':
						phi = r.firstChild.data.decode("utf-8").split()
					elif r.nodeName == 'cotTheta':
						data = r.firstChild.data.decode("utf-8").split()
						eta = convertEta(data)
					elif r.nodeName == 'polylineX':
						xPoints = r.firstChild.data.decode("utf-8").split()
					elif r.nodeName == 'polylineY':
						yPoints = r.firstChild.data.decode("utf-8").split()
					elif r.nodeName == 'polylineZ':
						zPoints = r.firstChild.data.decode("utf-8").split()
					elif r.nodeName == 'numPolyline':
						numPolyLines = r.firstChild.data.decode("utf-8").split()
				count+=1
	

		
	pointsCollection = getPoints(xPoints, yPoints, zPoints)
	#add values to collections:
	collectionsTemp = []
	associations = createAssociations(numPolyLines)
	for i in range(len(pt)):
		collectionsTemp.append(float(pt[i]))
		collectionsTemp.append(int(charge))
		collectionsTemp.append(rp)
		collectionsTemp.append(float(phi[i]))
		collectionsTemp.append(eta[i])
		collectionsTemp.append(int(caloEnergy))
		collections.append(collectionsTemp)
		collectionsTemp = []

	return collections, pointsCollection, associations

# Write data as JSON
def writeJson(collections, pointsCollection, associations, filename):
	typeData = {"AtlasTracks_V1": [["pt", "double"],["charge", "int"],["rp", "v3d"],["phi", "double"],["eta", "double"],["calo_energy", "double"]], "Points_V2": [["pos", "v3d"]]}
	typeData = coll.OrderedDict(reversed(list(typeData.items())))
	collectionData = {"AtlasTracks_V1": collections, "Points_V2": pointsCollection}
	collectionData = coll.OrderedDict(reversed(list(collectionData.items())))
	associationData = {"MuonGlobalPoints_V2": associations}
	#Types, Collections, Associations are general format. No idea what Associations do
	total = {u"Types": typeData, u"Collections": collectionData, u"Associations": associationData}
	total = coll.OrderedDict(reversed(list(total.items())))
	fileNoExt = os.path.splitext(filename)[0]
	fileNoExt = fileNoExt + '.json'
	with io.open(fileNoExt, 'w', encoding='utf-8') as f:
	  f.write(json.dumps(total, ensure_ascii=False))

def main():
	# Iterate over all XML files in current directory
	for filename in glob.glob('*.xml'):
		#open XML doc getting elements tagged <Track ...>
		xmldoc = minidom.parse(filename)
		itemlist = xmldoc.getElementsByTagName('Track')
		collections, pointsCollection, associations = collectTracks(itemlist)
		#convert to JSON format and write to file
		writeJson(collections, pointsCollection, associations, filename)	


main()