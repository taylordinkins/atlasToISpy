# Parse all primary tag sections in XML file
from xml.dom import minidom

# Change filename as required
filename = 'JiveXML_284484_731223307.xml'

xmldoc = minidom.parse(filename)
rootElem = xmldoc.documentElement
itemlist = rootElem.childNodes
count = 0
for s in itemlist:
    if (count % 2) != 0:
        print(s.nodeName)
        if(s.hasAttributes()):
            for r in s.attributes.items():
                print '***',
                print(r)
    count+=1

