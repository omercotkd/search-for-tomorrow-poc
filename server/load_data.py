from etl.n12 import N12Document
from etl.nafshi import NafshiDocument
import json

with open("/Users/lnachman/Documents/search-for-tomorrow-poc/nafshi.json") as f:
    nafshi_data = json.load(f)["items"]

with open("/Users/lnachman/Documents/search-for-tomorrow-poc/n12.json") as f:
    n12_data = json.load(f)


nafshi_data = NafshiDocument.from_list(nafshi_data)

n12_data = N12Document.from_list(n12_data)

for item in nafshi_data:
    item.into_document().save()

for item in n12_data:
    item.into_document().save()


