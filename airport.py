import json
import sys
# for command line manipulation
import argparse
# for simple http request
import urllib
import requests
# for calculations and sorting
from math import pow
from math import sqrt
from operator import itemgetter


class Request_Handler:
    def __init__(self):
        self.base_url = "https://mikerhodes.cloudant.com"
        self.database = "airportdb"
        self.search_path = "/_design/view1/_search"

    def __call__(self, client_inputs):
        query = "geo?q=lon:[" + str(client_inputs.longitude - client_inputs.distance) + " TO " + str(client_inputs.longitude + client_inputs.distance) + "] AND lat:[" + str(client_inputs.latitude - client_inputs.distance) + " TO " + str(client_inputs.latitude + client_inputs.distance) + "]"
        encoded_url = urllib.quote(self.base_url + "/" + self.database + self.search_path + "/" + query, ":[]/?=")
        http_response = requests.get(url=encoded_url)
        if http_response.status_code != 200:
            raise Exception("HTTP request failed status code: " + str(http_response.status_code) + ", content: " + http_response.content)
        return http_response.content


class Logic:
    def __init__(self):
        self.handle = Request_Handler()

    def __call__(self, client_inputs):
        if client_inputs.distance < 0:
            raise Exception("The provided distance can not be a negative value!")
        if -180 > client_inputs.longitude and client_inputs.longitude > 180:
            raise Exception("The longitude coordinate should between -180 and 180!")
        if -90 > client_inputs.latitude and client_inputs.latitude > 90:
            raise Exception("The latitude coordinate should between -90 and 90!")
        server_response = self.handle(client_inputs)
        airports_unsorted = self.get_relevant_search_result(server_response, client_inputs)
        airports_sorted = sorted(airports_unsorted, key=itemgetter('distance'))
        return airports_sorted

    def calculate_distance(self, parse_result, lat, lon):
        return sqrt(pow(abs(parse_result.latitude - lat), 2) + pow(abs(parse_result.longitude - lon), 2))

    def get_relevant_search_result(self, server_response, client_inputs):
        relevant_airports = []
        unmarshalled_result = json.loads(server_response)
        if "rows" in unmarshalled_result:
            for airport in unmarshalled_result["rows"]:
                if "fields" in airport and "lat" in airport["fields"] and "lon" in airport["fields"]:
                    current_airfield_distance = self.calculate_distance(client_inputs, airport["fields"]["lat"],
                                                                airport["fields"]["lon"])
                    if current_airfield_distance <= client_inputs.distance:
                        airport["distance"] = current_airfield_distance
                        relevant_airports.append(airport)
        return relevant_airports


class View:
    def __call__(self, sorted_airports):
        for airport in sorted_airports:
            if ("fields" in airport) and ("name" in airport["fields"]) and ("lat" in airport["fields"]) and ("lon" in airport["fields"]) and ("distance" in airport):
                print("Name: " + airport["fields"]["name"] + ", pos: (lat: " + str(
                    airport["fields"]["lat"]) + ", lon: " + str(
                    airport["fields"]["lon"]) + "), distance from user given point: " + str(airport["distance"]))

class Airport:
    def __init__(self, prog):
        self.prog = prog
        self.business_logic = Logic()
        self.view = View()

    def __call__(self, args):
        parser = argparse.ArgumentParser(description='Search closest airports', prog=self.prog)
        parser.add_argument('-lon', '--longitude',
                            required=True,
                            type=float,
                            help='The longitude coordinate. (between -180 and 180)',
                            action='store')
        parser.add_argument('-lat', '--latitude',
                            required=True,
                            type=float,
                            help='The latitude coordinate. (between -90 and 90)',
                            action='store')
        parser.add_argument('-dis', '--distance',
                            required=True,
                            type=float,
                            help='The radius of the search from the given longitude and latitude point. (positive number)',
                            action='store')
        client_inputs = parser.parse_args(args)
        airports = self.business_logic(client_inputs)
        self.view(airports)

def main():
    processor = Airport('airport')
    args = sys.argv[1:]
    try:
        processor(args)
    except Exception as exp:
        print('Got error %s' % str(exp))
        sys.exit(1)


if __name__ == '__main__':
    main()

