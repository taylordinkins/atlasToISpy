# JiveXML parsing (avoid scrolling through 200k lines)
from xml.dom import minidom
from sets import Set

# Change filename and tagname as required
filename = 'JiveXML_284484_731223307.xml'
tagname = 'LAr'

xmldoc = minidom.parse(filename)
itemlist = xmldoc.getElementsByTagName(tagname)
print(len(itemlist))
for s in itemlist:
    print 'Parent ', 
    print(s.nodeName)
    print(s.attributes['count'].value)
    print(s.attributes['storeGateKey'].value)
    count = 0
    for r in s.childNodes:
        if (count % 2) != 0:
            print'Child ',
            print(r.nodeName)
            # Add desired code here to check data for specific children
        count+=1
