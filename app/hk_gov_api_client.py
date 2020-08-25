import requests


class HkGovApiClient(object):
    def __init__(self):
        self.buildings_url = "https://api.data.gov.hk/v2/filter"
        self.location_url = "https://www.als.ogcio.gov.hk/lookup"
        self.totals_params = {
            "q": '{"resource":"http://www.chp.gov.hk/files/misc/latest_situation_of_reported_cases_covid_19_eng.csv","section":1,"format":"json","sorts":[[3,"desc"]]}'}
        self.building_params_en = {
            "q": '{"resource": "http://www.chp.gov.hk/files/misc/building_list_eng.csv", "section": 1, "format": "json", "filters": [[3, "ct", ["20"]]]}'
        }
        self.building_params_zh = {
            "q": '{"resource": "http://www.chp.gov.hk/files/misc/building_list_chi.csv", "section": 1, "format": "json", "filters": [[3, "ct", ["20"]]]}'
        }
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en,zh'}

    def get(self, url, params):
        response = requests.get(url=url, params=params, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data

    def get_covid_buildings(self):
        buildings_en = self.get(self.buildings_url, self.building_params_en)
        buildings_zh = self.get(self.buildings_url, self.building_params_zh)

        return buildings_en, buildings_zh

    def get_totals(self):
        totals = self.get(self.buildings_url, self.totals_params)
        most_recent_total = totals[0]
        prev_total = totals[1]
        cases = {
            "today": most_recent_total['Number of confirmed cases'] - prev_total['Number of confirmed cases'],
            "total": most_recent_total['Number of confirmed cases']
        }
        deaths = {
            "today": most_recent_total['Number of death cases'] - prev_total['Number of death cases'],
            "total": most_recent_total['Number of death cases']
        }
        return {"deaths": deaths, "cases": cases}

    def get_potential_locations(self, district, building):
        query = "{building}, {district} district".format(
            district=district, building=building)
        params = {"q": query}
        data = self.get(url=self.location_url, params=params)
        if "SuggestedAddress" not in data:
            return []
        suggestions = data["SuggestedAddress"]
        return suggestions
