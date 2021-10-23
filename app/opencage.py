from pprint import pprint
from opencage.geocoder import OpenCageGeocode


class OpenCageClient:
    API_KEY = '5dd1b2de544444e7aefb94afd0ce71e5'

    def __init__(self):
        self.geocoder = OpenCageGeocode(self.API_KEY)

    def geocode(self, address):
        query = u'Bosutska ulica 10, Trnje, Zagreb, Croatia'
        results = self.geocoder.geocode(query)
        print(u'%f;%f;%s;%s' % (results[0]['geometry']['lat'],
                                results[0]['geometry']['lng'],
                                results[0]['components']['country_code'],
                                results[0]['annotations']['timezone']['name']))

