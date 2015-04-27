import xml.etree.ElementTree as ET
import re
filename = "0NanoDegree/atlanta.osm"
nodeTypes = set()
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
for event, elem in ET.iterparse(filename):
  if elem.tag == "tag":
    if elem.attrib['k'] == "addr:street":
      m = street_type_re.search(elem.attrib['v'])
      if m:
        name = m.group()
        nodeTypes.add(name)
  elem.clear()
print nodeTypes

