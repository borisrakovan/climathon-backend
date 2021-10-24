from pprint import pprint

from opencage.geocoder import OpenCageGeocode


class AddressNotFound(Exception):
    pass


class OpenCageClient:
    API_KEY = '212a30196457498c9b9e30e46ea543fc'

    def __init__(self):
        self.geocoder = OpenCageGeocode(self.API_KEY)

    def geocode(self, address):
        results = self.geocoder.geocode(address)
        if len(results) == 0:
            raise AddressNotFound()

        return results[0]['geometry']['lat'], results[0]['geometry']['lng']

    def reverse_geocode(self, lat, long):
        results = self.geocoder.reverse_geocode(lat, long)
        return results

