import pandas as pd
import requests

data = pd.read_csv('data_points_20180102.txt', delimiter=':|  Bearing:', names=['tipo', 'valores', 'bearing'], header=None)

GOOGLE_MAPS_API_KEY = 'AIzaSyCeWfCykKZLpMrg83oDcRoto_Aw4mHsyZM'

def address_resolver(json, dataFrame):
    final = {}
    data = {}
    for item in json['address_components']:
        for category in item['types']:
            data[category + '_long'] = item['long_name']
            data[category + '_short'] = item['short_name']

    dataFrame['rua'] = data.get("route_long", None)
    dataFrame['estado'] = data.get("administrative_area_level_1_short", None)
    dataFrame['cidade'] = data.get("administrative_area_level_2_long", None)
    dataFrame['pais'] = data.get("country_long", None)
    dataFrame['cep'] = data.get("postal_code_long", None)
    dataFrame['bairro'] = data.get("sublocality_long",None)
    dataFrame['numero'] = data.get('street_number_long', None)

def busca_endereco(dataFrame):
    latitude=dataFrame['latitude']
    longitude=dataFrame['longitude']

    print('\n')
    print('{lat},{lon}'.format(lat=latitude, lon=longitude))

    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&language=pt-BR&result_type=street_address&key={key}".format(
        lat=latitude,
        lon=longitude,
        key=GOOGLE_MAPS_API_KEY
    )
    url = "{base}{params}".format(base=base, params=params)
    print(url)
    response = requests.get(url).json()
    status = response['status']
    print(status)
    if status == 'OK':
        results = response['results']
        address_resolver(results[0], dataFrame)

data = data.join(data['valores'].str.split('   ', 1, expand=True).rename(columns={0:'graus', 1:'decimal'}))

print(data.to_string().encode('utf-8').decode('latin-1'))

latitudes = data[data['tipo'].str.contains('Latitude')]
longitudes = data[data['tipo'].str.contains('Longitude')]
distances = data[data['tipo'].str.contains('Distance')]
latitudes = latitudes.reset_index()
longitudes = longitudes.reset_index()
distances = distances.reset_index()
print(latitudes.to_string().encode('utf-8').decode('latin-1'))
print(longitudes.to_string().encode('utf-8').decode('latin-1'))
print(distances.to_string().encode('utf-8').decode('latin-1'))

colunas = ['latitude', 'longitude', 'rua', 'numero', 'bairro', 'cidade', 'cep', 'estado', 'pais', 'latitudeGraus', 'longitudeGraus', 'distancia', 'bearing']
df = pd.DataFrame(columns=colunas)
df['latitude'] = latitudes['decimal']
df['longitude'] = longitudes['decimal']
df['latitudeGraus'] = latitudes['graus']
df['longitudeGraus'] = longitudes['graus']
df['distancia'] = distances['valores']
df['bearing'] = distances['bearing']
# print(df.to_string().encode('utf-8').decode('latin-1'))



df.apply(lambda x: busca_endereco(x), axis=1)
print('\n')
print(df)
# df['rua'],df['numero'],df['bairro'],df['cidade'],df['estado'],df['cep'],df['pais'] = busca_endereco(lat, lon)
