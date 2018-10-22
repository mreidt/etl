import pandas as pd
import requests
import pathlib
from log import get_logger
from decouple import config, Csv
from exceptions import GMAPSError, LatitudeWrongValue, LongitudeWrongValue

logger = get_logger('logger')

def busca_endereco(dataFrame):
    latitude=dataFrame['LATITUDE']
    longitude=dataFrame['LONGITUDE']
    checkLatitude(latitude=latitude)
    checkLongitude(longitude=longitude)

    logger.info('Searching for latitude: {lat}, longitude: {lon}'.format(lat=latitude, lon=longitude))

    base = config('GOOGLE_MAPS_BASE_URL')
    params = "latlng={lat},{lon}&language=pt-BR&result_type=street_address&key={key}".format(
        lat=latitude,
        lon=longitude,
        key=config('GOOGLE_MAPS_API_KEY')
    )
    url = "{base}{params}".format(base=base, params=params)
    logger.debug('GMAPS URL: {url}'.format(url=url))
    response = requests.get(url).json()
    status = response['status']
    logger.debug('GMAPS STATUS: {status}'.format(status=status))
    if status == 'OK':
        results = response['results']
        addressResolver(results[0], dataFrame)
    elif status == 'ZERO_RESULTS':
        logger.info('The request for {lat},{lon} returned no results!'.format(lat=latitude, lon=longitude))
    else:
        raise GMAPSError('Google Maps API returned {status}, for {lat},{lon}'.format(status=status,lat=latitude,lon=longitude))

def addressResolver(json, dataFrame):
    final = {}
    data = {}
    try:
        for item in json['address_components']:
            for category in item['types']:
                data[category + '_long'] = item['long_name']
                data[category + '_short'] = item['short_name']
    except KeyError:
        raise KeyError('No {error} found!'.format(error=KeyError))

    try:
        dataFrame['RUA'] = data.get("route_long", None)
        dataFrame['ESTADO'] = data.get("administrative_area_level_1_short", None)
        dataFrame['CIDADE'] = data.get("administrative_area_level_2_long", None)
        dataFrame['PAIS'] = data.get("country_long", None)
        dataFrame['CEP'] = data.get("postal_code_long", None)
        dataFrame['BAIRRO'] = data.get("sublocality_long",None)
        dataFrame['NUMERO'] = data.get('street_number_long', None)
    except TypeError:
        raise TypeError()

def fileType(filename):
    return ''.join(pathlib.Path(filename).suffixes)

def checkLatitude(latitude):
    latitude = float(latitude)
    if latitude >= -90 and latitude <= 90:
        return True
    else:
        raise LatitudeWrongValue('{lat} is not a valid latitude'.format(lat=latitude))

def checkLongitude(longitude):
    longitude = float(longitude)
    if longitude >= -180 and longitude <= 180:
        return True
    else:
        raise LongitudeWrongValue('{lon} is not a valid longitude'.format(lon=longitude))
