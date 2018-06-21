from pymongo import MongoClient
import matplotlib.pyplot as plt
import io
import base64
import bson
import json

image_loc = 'C:\\Users\\jcochran\\Desktop\\uhcsdata\\micrographs\\'

client = MongoClient()

db = client.micrographs


micrograph_image_collection = db.micrograph_image_collection

plt.gray()
j = 0
for m in micrograph_image_collection.find():
    format = m['format']
    if j <= 5:
        new_binary = io.BytesIO(base64.b64decode(m['image']))
        img = plt.imread(new_binary, format=format)
        plt.imshow(img)
        plt.show()
    j += 1