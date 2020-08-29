
from app.hk_gov_api_client import HkGovApiClient
from app.building import Building
from app.timestamp import Timestamp
import geocoder
import json
import jsonpickle
import os

api_client = HkGovApiClient()
raw_buildings_en, raw_buildings_zh = api_client.get_covid_buildings()
buildings = [Building(raw_data_en, raw_data_zh) for raw_data_en, raw_data_zh in zip(
    raw_buildings_en, raw_buildings_zh)]


buildings_dict = []
districts = {}
for building in buildings:
    query = "{building}, {district} district, Hong Kong".format(
        district=building.district, building=building.name)
    g = geocoder.google(query, key=os.environ['GOOGLE_API_KEY'])
    building_dict = building.return_as_dict()
    building_dict['address'] = g.address
    building_dict['lat'] = g.lat
    building_dict['lng'] = g.lng
    building_dict['confidence'] = g.confidence
    buildings_dict.append(building_dict)

    district = building_dict['district']
    if district in districts:
        districts[district].update(building_dict['cases'])
    else:
        districts[district] = set(building_dict['cases'])


districts_final = {key: len(val)
                   for key, val in districts.items()}

with open('app/district_locations.json', encoding='utf-8') as f:
    districts_loc = json.load(f)

for district in districts_loc:
    name = district['center']['properties']['name'].replace(
        '_And_', ' & ').replace('_', ' ')
    if name in districts_final:
        district['center']['properties']['cases'] = districts_final[name]
    else :
        district['center']['properties']['cases'] = districts_final[name] = 0


totals = api_client.get_totals()
t = Timestamp.get_hk_time()
data = {'districts': districts_loc, 'buildings': buildings_dict,
        'timestamp': t, 'totals': totals}

frozen = jsonpickle.encode(data)
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(frozen)
