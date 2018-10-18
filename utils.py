import pandas as pd
import requests
from decouple import config, Csv

def busca_endereco(dataFrame):
    latitude=dataFrame['LATITUDE']
    longitude=dataFrame['LONGITUDE']

    print('\n')
    print('{lat},{lon}'.format(lat=latitude, lon=longitude))

    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&language=pt-BR&result_type=street_address&key={key}".format(
        lat=latitude,
        lon=longitude,
        key=config('GOOGLE_MAPS_API_KEY')
    )
    url = "{base}{params}".format(base=base, params=params)
    print(url)
    response = requests.get(url).json()
    status = response['status']
    print(status)
    if status == 'OK':
        results = response['results']
        address_resolver(results[0], dataFrame)

def address_resolver(json, dataFrame):
    final = {}
    data = {}
    for item in json['address_components']:
        for category in item['types']:
            data[category + '_long'] = item['long_name']
            data[category + '_short'] = item['short_name']

    dataFrame['RUA'] = data.get("route_long", None)
    dataFrame['ESTADO'] = data.get("administrative_area_level_1_short", None)
    dataFrame['CIDADE'] = data.get("administrative_area_level_2_long", None)
    dataFrame['PAIS'] = data.get("country_long", None)
    dataFrame['CEP'] = data.get("postal_code_long", None)
    dataFrame['BAIRRO'] = data.get("sublocality_long",None)
    dataFrame['NUMERO'] = data.get('street_number_long', None)
