import xml.etree.cElementTree as ET
from collections import defaultdict
import re
from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.test
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

for street in  db.city.find({"address.postcode": {"$regex": "GA" }}):
	cityCode = street[u'address'][u'postcode']
	#street_type = "Avenue"
	name = re.sub(r"GA", '', cityCode)
	street[u'address'][u'postcode'] = name
	print name
	db.city.save(street)

