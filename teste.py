import pandas as pd
import requests
from sqlalchemy import create_engine
from pandas.io import sql

data = pd.read_csv('data_points_20180101.txt', delimiter=':|  Bearing:', names=['tipo', 'valores', 'bearing'], header=None)

GOOGLE_MAPS_API_KEY = 'AIzaSyCeWfCykKZLpMrg83oDcRoto_Aw4mHsyZM'
columns = ['LATITUDE', 'LONGITUDE', 'RUA', 'NUMERO', 'BAIRRO', 'CIDADE', 'CEP', 'ESTADO', 'PAIS', 'LATITUDEGRAUS', 'LONGITUDEGRAUS', 'DISTANCIA', 'BEARING']
db_user = 'root'
db_password = '*Gm299002'

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

def busca_endereco(dataFrame):
    latitude=dataFrame['LATITUDE']
    longitude=dataFrame['LONGITUDE']

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

# colunas = ['latitude', 'longitude', 'rua', 'numero', 'bairro', 'cidade', 'cep', 'estado', 'pais', 'latitudeGraus', 'longitudeGraus', 'distancia', 'bearing']
df = pd.DataFrame(columns=columns)
df['LATITUDE'] = latitudes['decimal']
df['LONGITUDE'] = longitudes['decimal']
df['LATITUDEGRAUS'] = latitudes['graus']
df['LONGITUDEGRAUS'] = longitudes['graus']
df['DISTANCIA'] = distances['valores']
df['BEARING'] = distances['bearing']
# print(df.to_string().encode('utf-8').decode('latin-1'))



df.apply(lambda x: busca_endereco(x), axis=1)
print('\n')
print(df)

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user=db_user,
                               pw=db_password,
                               db="ETLDB"))
# df['rua'],df['numero'],df['bairro'],df['cidade'],df['estado'],df['cep'],df['pais'] = busca_endereco(lat, lon)
df.to_sql(con=engine, name='ENDERECOS', if_exists='append', index=False)


# (latitude, longitude, rua, numero, bairro, cidade, cep, estado, pais, `latitudeGraus`, `longitudeGraus`, distancia, bearing)
