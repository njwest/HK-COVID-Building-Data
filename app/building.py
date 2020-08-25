import re
import datetime
from collections import namedtuple

Address = namedtuple(
    'Address', ['building', 'street', 'street_no', 'district'])


class Building(object):
    def __init__(self, raw_data, raw_data_zh):
        self.district = raw_data["District"]
        self.name = Building.parse_raw_name(raw_data["Building name"])
        self.name_zh = Building.parse_raw_name_zh(raw_data_zh["大廈名單"])
        self.residential = Building.is_residential(raw_data["Building name"])
        self.kind = Building.get_kind(
            self.residential, raw_data["Building name"])
        self.date = Building.parse_date(
            raw_data["Last date of residence of the case(s)"])
        self.case_count = Building.count_cases(
            raw_data["Related probable/confirmed cases"])
        self.cases = raw_data["Related probable/confirmed cases"].split(',')

    def set_location(self, raw_location):
        self.accuracy = raw_location['ValidationInformation']['Score']
        self.raw_address = raw_location['Address']['PremisesAddress']
        self.location_en = Building.parse_location(
            'Eng', self.raw_address)._asdict()
        self.location_cn = Building.parse_location(
            'Chi', self.raw_address)._asdict()
        self.geo_location = Building.parse_geo_location(
            self.raw_address)

    def return_as_dict(self):
        return {
            'district': self.district,
            'name': self.name,
            'name_zh': self.name_zh,
            'residential': self.residential,
            'kind': self.kind,
            'date': self.date,
            'cases': self.cases}

    @staticmethod
    def parse_location(lang_prefix, location):
        raw_address = location[lang_prefix + 'PremisesAddress']
        building = Building.format_name(raw_address['BuildingName'])
        street_name = Building.format_name(
            raw_address[lang_prefix + 'Street']['StreetName'])
        street_no = raw_address[lang_prefix + 'Street']['BuildingNoFrom']
        district = Building.format_name(
            raw_address[lang_prefix + 'District']['DcDistrict'])
        return Address(building, street_name, street_no, district)

    @staticmethod
    def parse_geo_location(location):
        geo_location_raw = location['GeospatialInformation']
        geo_location = {
            'lat': geo_location_raw['Latitude'], 'long': geo_location_raw['Longitude']}
        return geo_location

    @ staticmethod
    def format_name(name):
        return name.lower().title()

    @ staticmethod
    def parse_raw_name(name):
        name = re.sub("([^\x00-\x7F])+", " ", name)
        name = name.replace("(non-residential)", "")
        return name.strip()

    @ staticmethod
    def parse_raw_name_zh(name):
        name = name.replace("(非住宅)", "")
        return name.strip()

    @ staticmethod
    def is_residential(name):
        return "(non-residential)" not in name

    @ staticmethod
    def get_kind(residential, name):
        if residential:
            return 'residential'
        name_lower = name.lower()
        if 'hospital' in name_lower:
            return 'hospital'
        for keyword in ['shopping', 'mall', 'commercial']:
            if keyword in name_lower:
                return 'mall'
        for keyword in ['restaurant', 'caf', 'kitchen', 'pizza']:
            if keyword in name_lower:
                return 'restaurant'
        return 'non-residential'

    @ staticmethod
    def parse_date(date_string):
        return date_string
        split_string = [int(x) for x in date_string.split('/')]
        date = datetime.datetime(
            split_string[2], split_string[1], split_string[0])
        return date

    @ staticmethod
    def count_cases(case_string):
        return len(case_string.split(','))
