from os.path import dirname, abspath, join
import json
import base64
import bson
import PIL
from io import BytesIO
from mongoengine import connect
from schema import Micrograph, Sample, User
#
# Get paths
root_dir = dirname(abspath(__file__))
data_dir = join(root_dir, 'data')
micrograph_dir = join(data_dir, 'micrographs')
#
# Get file names
micrograph_metadata_file_name = join(data_dir, 'micro_db.json')
sample_metadata_file_name = join(data_dir, 'sample_db.json')
user_metadata_file_name = join(data_dir, 'user_db.json')
#
# Connect to db
connect('micrograph_db')
#
# Load user info
with open(user_metadata_file_name, 'r') as user_metadata_file:
    user_metadata = json.load(user_metadata_file)
    for k, v in user_metadata.items():
        user = User(
            user_id=int(k),
            user_name=v['user_name'],
            first_name=v['first_name'],
            last_name=v['last_name'],
            email=v['email'],
        ).save()
#
# Load sample info
with open(sample_metadata_file_name, 'r') as sample_metadata_file:
    sample_metadata = json.load(sample_metadata_file)
    for k, v in sample_metadata.items():
        sample = Sample(
            sample_id=int(k),
            anneal_temperature=v['anneal_temperature'],
            anneal_time_units=v['anneal_time_units'],
            label=v['label'],
            anneal_time=v['anneal_time'],
            cooling_method=v['cooling_method'],
            anneal_temperature_units=v['anneal_temperature_units'],
        ).save()
#
# Load micrograph info
with open(micrograph_metadata_file_name, 'r') as micrograph_metadata_file:
    micrograph_metadata = json.load(micrograph_metadata_file)
    for k, v in micrograph_metadata.items():
        #
        # Retrieve referenced documents
        contributor = User.objects.get(user_id=v['contributor_key'])
        sample = None
        if v['sample_key'] is not None:
            sample = Sample.objects.get(sample_id=v['sample_key'])
        #
        # Load images
        image_file_name = join(micrograph_dir, v['file_name'])
        with open(image_file_name, 'rb') as image_file:
            img = PIL.Image.open(image_file)
            w,h = img.size
            #
            # Crop the images to remove scale bar at bottom
            cropped_img = img.crop((0, 0, w, h - 38))
            cropped_binary = BytesIO()
            cropped_img.save(
                        cropped_binary,
                        format=img.format
            )
            #
            # Encode images as b64
            encoded_image_binary = bson.binary.Binary(
                base64.b64encode(
                    cropped_binary.getvalue()
                )
            )
        #
        # Construct micrograph document
        micrograph = Micrograph(
            micrograph_id=int(k),
            sample=sample,
            contributor=contributor,
            magnification=v['magnification'],
            micron_bar=v['micron_bar'],
            micron_bar_pixels=v['micron_bar_pixels'],
            micron_bar_units=v['micron_bar_units'],
            file_name=v['file_name'],
            detector=v['detector'],
            primary_microconstituent=v['primary_microconstituent'],
            image=encoded_image_binary
        ).save()
        