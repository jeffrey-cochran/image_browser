from mongoengine import *

class Micrograph(Document):
    micrograph_id = IntField(primary_key=True)
    sample = ReferenceField('Sample')
    magnification = StringField() 
    micron_bar = FloatField()
    micron_bar_pixels = IntField()
    micron_bar_units = StringField()
    file_name = StringField()
    detector = StringField()
    primary_microconstituent = StringField()
    contributor = ReferenceField('User')
    image = BinaryField()

class Sample(Document):
    sample_id = IntField(primary_key=True)
    anneal_temperature = FloatField()
    anneal_time_units = StringField()
    label = StringField()
    anneal_time = FloatField()
    cooling_method = StringField()
    anneal_temperature_units = StringField()
    
class User(Document):
    user_id = IntField(primary_key=True)
    user_name = StringField()
    first_name = StringField()
    last_name = StringField()
    email = StringField()
