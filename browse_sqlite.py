import sqlite3
import json

conn = sqlite3.connect('C:\Users\jcochran\Desktop\uhcsdata\microstructures.sqlite')
c = conn.cursor()
d = {}
for row in c.execute("SELECT * FROM sample;"):


with open('sample_db.json', 'w') as json_file:
    json.dump(d, json_file, indent=4)
    
    # [
    #     sample_id,
    #     label,
    #     anneal_time,
    #     anneal_time_units,
    #     anneal_temperature,
    #     anneal_temperature_units,
    #     cooling_method,
    # ] = row

    # d[sample_id] = {
    #     'label': label,
    #     'anneal_time': anneal_time,
    #     'anneal_time_units': anneal_time_units,
    #     'anneal_temperature': anneal_temperature,
    #     'anneal_temperature_units': anneal_temperature_units,
    #     'cooling_method': cooling_method,
    # }

    # [
    #     micrograph_id,
    #     file_name,
    #     micron_bar,
    #     micron_bar_units,
    #     micron_bar_pixels,
    #     magnification,
    #     detector,
    #     sample_key,
    #     contributor_key,
    #     primary_microconstituent
    # ] = row

    # d[micrograph_id] = {
    #     'file_name': file_name,
    #     'micron_bar': micron_bar,
    #     'micron_bar_units': micron_bar_units,
    #     'micron_bar_pixels': micron_bar_pixels,
    #     'magnification': magnification,
    #     'detector': detector,
    #     'sample_key': sample_key,
    #     'contributor_key': contributor_key,
    #     'primary_microconstituent': primary_microconstituent
    # }