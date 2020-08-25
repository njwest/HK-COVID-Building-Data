import json

with open('data.json') as file:
    buildings = json.load(file)

districts = {}
for building in buildings:
    district = building['district']
    if district in districts:
        districts[district].update(building['cases'])
    else:
        districts[district] = set(building['cases'])

districts_final = [{key: len(val)} for key, val in districts.items()]

data = {'districts': districts_final, 'buildings': buildings}

with open('data2.json', 'w') as output_file:
    json.dump(data, output_file)
