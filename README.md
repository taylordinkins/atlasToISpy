Thanks to CMS for providing the event display iSpy. 

iSpy is ran in browser using WebGL, and all information is found here:
https://cms-outreach.github.io/ispy/

For my additions:

1. Scripts will be ran from same directory as files (XML or JSON) - python [scriptname].py

2. iSpy will read converted JSON data from a .zip which must have the format: 
	/PATH/TO/iSpy/ispy-webgl/data/<dirName>/Events/<runName>/data.json
	One will need to compress the directory <dirName> and open <dirName>.zip in iSpy browser

3. collectCalos.py is unfinished and not clean. It is included only for reference if necessary.
	
4. Actual calorimeters will need to be hardcoded into a JSON format to be drawn using 8 corners method
	Subsequently, energy data from XML file will scale the distance of calos
	ID data from XML file will "activate" which hardcoded calos are displayed (incomplete as of May, 2017)

5. Calorimeter objects for Atlas may need to be added into the 'objects-config.js'

6. Calorimeter draw technique can be changed in 'objects-draw.js' in /path/to/iSpy/ispy-webgl/js
	If needed...
