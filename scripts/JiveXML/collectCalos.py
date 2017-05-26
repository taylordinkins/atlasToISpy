# Collect Tracks and eventually calos from Atlas data
# Convert to JSON
# Save as .json file
# INCOMPLETE AND INCORRECT for Calos 

import json, io, collections as coll
from xml.dom import minidom
import math

atlasTrackIndex = 0
atlasPointIndex = 2
thetaVals = []
numPolyLines = []

#ecal stuff up here for direct access
ecalThetas = []
ecalFront1 = []
ecalFront2 = []
ecalFront3 = []
ecalFront4 = []
ecalBack1 = []
ecalBack2 = []
ecalBack3 = []
ecalBack4 = []
ecalScaling = 0.0425

def convertEta(data):
	retVal = []
	for elem in data:
		theta = (math.pi/2) - math.atan(float(elem))
		thetaVals.append(theta)
		retVal.append(-math.log(math.tan(theta/2)))
	return retVal

def convertTheta(data):
	for elem in data:
		theta = 2*math.atan(math.exp(-float(elem)))
		ecalThetas.append(math.pi/2 - theta)

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

def ecalPoints(phi, energy, etas):
	for i in range(len(energy)):
		if float(energy[i]) >= 1.0:
			xPos = 1
			yPos = 1
			zPos = 1
			d = 1.5*math.log(float(energy[i]))
			
			x = math.cos(float(phi[i]))
			y = math.sin(float(phi[i]))
			z = math.sinh(float(etas[i]))/2
			print(z)
			if x < 0:
				xPos = -1
			if y < 0:
				yPos = -1
			if z < 0:
				zPos = -1
			ecalFront1.append([x,y,z])
			ecalFront2.append([x,y,z+(zPos*d*ecalScaling)])
			ecalFront3.append([x+(xPos*d*ecalScaling),y,z+(zPos*d*ecalScaling)])
			ecalFront4.append([x+(xPos*d*ecalScaling),y,z])
			ecalBack1.append([x,y+(yPos*d*ecalScaling),z])
			ecalBack2.append([x,y+(yPos*d*ecalScaling),z+(zPos*d*ecalScaling)])
			ecalBack3.append([x+(xPos*d*ecalScaling),y+(yPos*d*ecalScaling),z+(zPos*d*ecalScaling)])
			ecalBack4.append([x+(xPos*d*ecalScaling),y+(yPos*d*ecalScaling),z])

def main():
	#open XML doc getting elements tagged <Track ...>
	xmldoc = minidom.parse('JiveXML_284484_731223307.xml')
	tracklist = xmldoc.getElementsByTagName('Track')
	ecal = xmldoc.getElementsByTagName('LAr')
	#Track Collections variables
	trackCollections = []
	retData = []
	pt = []
	phi = []
	eta = []
	xPoints = []
	yPoints = []
	zPoints = []
	pointsCollection = []
	associations = []
	#FIX THIS LATER
	charge = 1
	rp = [0, 0, 0]
	caloEnergy = 0

	#iterate over all tags, currently looking for storeGateKey = 'Tracks' only, but will need to do for all:
	#08/06/2016

	#likely will need to be re-written for general cases since nodeNames may change and more subtags may be present

	for s in tracklist:
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
		trackCollections.append(collectionsTemp)
		collectionsTemp = []


	ecalEnergy = []
	ecalEta = []
	ecalPhi = []
	ecalTime = 1
	ecalDetId = []
	ecalCollection = []
	for s in ecal:
		if s.attributes['storeGateKey'].value == 'AllCalo':
			count = 0
			for r in s.childNodes:
				if (count % 2) != 0:
					if r.nodeName == 'energy':
						ecalEnergy = r.firstChild.data.decode("utf-8").split()
					elif r.nodeName == 'eta':
						ecalEta = r.firstChild.data.decode("utf-8").split()
						convertTheta(ecalEta)
					elif r.nodeName == 'phi':
						ecalPhi = r.firstChild.data.decode("utf-8").split()
					elif r.nodeName == 'id':
						ecalDetId = r.firstChild.data.decode("utf-8").split()
				count+=1

	ecalPoints(ecalPhi, ecalEnergy, ecalEta)
	collectionsTemp = []
	cornerIndex = 0
	for i in range(len(ecalEnergy)):
		if float(ecalEnergy[i]) >= 1.0:
			collectionsTemp.append(float(ecalEnergy[i]))
			collectionsTemp.append(float(ecalEta[i]))
			collectionsTemp.append(float(ecalPhi[i]))
			collectionsTemp.append(ecalTime)
			collectionsTemp.append(int(ecalDetId[i]))
			collectionsTemp.append(ecalFront1[cornerIndex])
			collectionsTemp.append(ecalFront2[cornerIndex])
			collectionsTemp.append(ecalFront3[cornerIndex])
			collectionsTemp.append(ecalFront4[cornerIndex])
			collectionsTemp.append(ecalBack1[cornerIndex])
			collectionsTemp.append(ecalBack2[cornerIndex])
			collectionsTemp.append(ecalBack3[cornerIndex])
			collectionsTemp.append(ecalBack4[cornerIndex])
			ecalCollection.append(collectionsTemp)
			collectionsTemp = []
			cornerIndex+=1


	
	

	#convert to JSON format and write to file
	#typeData is pasted from JSON file for Tracks. Not sure how to make general for all JSON Keys

	typeData = {"AtlasTracks_V1": [["pt", "double"],["charge", "int"],["rp", "v3d"],["phi", "double"],["eta", "double"],["calo_energy", "double"]], "Points_V2": [["pos", "v3d"]], "EBRecHits_V2": [["energy", "double"],["eta", "double"],["phi", "double"],["time", "double"],["detid", "int"],["front_1", "v3d"],["front_2", "v3d"],["front_3", "v3d"],["front_4", "v3d"],["back_1", "v3d"],["back_2", "v3d"],["back_3", "v3d"],["back_4", "v3d"]]}
	typeData = coll.OrderedDict(reversed(list(typeData.items())))
	collectionData = {"AtlasTracks_V1": trackCollections, "Points_V2": pointsCollection, "EBRecHits_V2": ecalCollection}
	collectionData = coll.OrderedDict(reversed(list(collectionData.items())))
	associationData = {"MuonGlobalPoints_V2": associations}
	#Types, Collections, Associations are general format. No idea what Associations do
	total = {u"Types": typeData, u"Collections": collectionData, u"Associations": associationData}
	total = coll.OrderedDict(reversed(list(total.items())))
	with io.open('withCalos.json', 'w', encoding='utf-8') as f:
	  f.write(json.dumps(total, ensure_ascii=False))
	


main()