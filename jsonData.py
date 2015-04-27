import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
attribs = ["addr:housenumber", "addr:postcode", "addr:street"]
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        if 'visible' in element.attrib: 
            node['visible'] = element.attrib['visible'] 
        node['created'] = {} 
        for i in CREATED: 
            node['created'][i] = element.attrib[i] 
        node['pos'] = [float(element.attrib[i]) for i in element.attrib if i == 'lon' or i == 'lat'] 
        node['pos'].sort(reverse=True) 
        node['type'] = element.tag 
        node['id'] = element.attrib['id'] 
        node['address'] = {elem.attrib['k'][5:]:elem.attrib['v'] for elem in element.iter('tag') if elem.attrib['k'] in attribs} 
        if node['address'] == {}: 
            node.pop("address", None) 
        if element.tag == "way": 
            node['node_refs'] = [elem.attrib['ref'] for elem in element.iter("nd")] 
        for elem in element.iter('tag'):
            if elem.attrib['k'] == "amenity":
                node['amenity'] = elem.attrib['v']
            if elem.attrib['k'] == "religion":
                node['religion'] = elem.attrib['v']
            if elem.attrib['k'] == "cuisine":   
                node['cuisine'] = elem.attrib['v']
            if elem.attrib['k'] == "gnis:created":    
                node['created'] = elem.attrib['v']
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return file_out

data = process_map('0NanoDegree/atlanta.osm', False)
print data
