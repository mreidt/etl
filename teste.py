import pandas as pd
import requests
from geopy.geocoders import Nominatim, GoogleV3, OpenCage, Pelias
import googlemaps

data = pd.read_csv('data_points_20180102.txt', delimiter=':|  Bearing:', names=['tipo', 'valores', 'bearing'], header=None)

GOOGLE_MAPS_API_KEY = 'AIzaSyCeWfCykKZLpMrg83oDcRoto_Aw4mHsyZM'
OPENCAGE_API_KEY = '530e319749ec479196567e19b3f479b2'

def separa_endereco(response, dataFrame):
    # R. Monsenhor Veras, 405 - Santana, Porto Alegre - RS, 90610-010, Brazil
    # TODO: verificar casos em que nao recebe o endereco completo
    print(response)

    # rua, numBairro, cidadeUf, cep, pais = response.split(',')
    # numero, bairro = numBairro.split('-')
    # cidade, uf = cidadeUf.split('-')
    #
    # dataFrame['rua']=rua
    # dataFrame['numero']=numero
    # dataFrame['bairro']=bairro
    # dataFrame['cidade']=cidade
    # dataFrame['estado']=uf
    # dataFrame['cep']=cep
    # dataFrame['pais']=pais

    print('--------------------\n')
    # return rua.strip(), numero.strip(), bairro.strip(), cidade.strip(), uf.strip(), cep.strip(), pais.strip()

def busca_dado(jsonData, dado):
    try:
        return jsonData[dado]
    except Exception:
        return None

def percorre_gmaps(dataGMaps):
    print(dataGMaps)
    for key, value in dataGMaps:
        print('{key}: {value}'.format(key=key, value=value))

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

    # geolocator_nominatim = Nominatim(user_agent="teste_matheus")
    # geolocator_opencage = Pelias()

    # location_nominatim = geolocator_nominatim.reverse("{lat}, {lon}".format(lat=latitude, lon=longitude), language='pt-BR')
    # location_opencage = geolocator_opencage.reverse("{lat}, {lon}".format(lat=latitude, lon=longitude))

    # geolocator = GoogleV3(api_key=GOOGLE_MAPS_API_KEY)
    # location = geolocator.reverse("{lat}, {lon}".format(lat=latitude, lon=longitude), language='pt-BR')
    print('\n')
    print('{lat},{lon}'.format(lat=latitude, lon=longitude))


    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    # # &result_type=street_address
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


    # gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    # reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude), language='pt-BR', result_type='street_address')

    # print(dados['rua'])
    # print(dados['uf'])
    # print(dados['cidade'])
    # print(dados['pais'])
    # print(dados['cep'])
    # print(dados['bairro'])
    # print(dados['numero'])




    # print(location.raw)
    # location_nominatim=location_nominatim.raw['address']

    # print(location_opencage)
    # location_opencage=location_opencage.raw['address']

    # rua = busca_dado(jsonData=location_nominatim, dado='road')
    # numero = busca_dado(jsonData=location_nominatim, dado='house_number')
    # bairro = busca_dado(jsonData=location_nominatim, dado='suburb')
    # cidade = busca_dado(jsonData=location_nominatim, dado='city')
    # estado = busca_dado(jsonData=location_nominatim, dado='state')
    # cep = busca_dado(jsonData=location_nominatim, dado='postcode')
    # pais = busca_dado(jsonData=location_nominatim, dado='country')

    # if not rua:
    #     rua = busca_dado(jsonData=location_opencage, dado='road')
    #
    # if not numero:
    #     numero = busca_dado(jsonData=location_opencage, dado='house_number')
    #
    # if not bairro:
    #     bairro = busca_dado(jsonData=location_opencage, dado='suburb')
    #
    # if not cidade:
    #     cidade = busca_dado(jsonData=location_opencage, dado='city')
    #
    # if not estado:
    #     estado = busca_dado(jsonData=location_opencage, dado='state')
    #
    # if not cep:
    #     cep = busca_dado(jsonData=location_opencage, dado='postcode')
    #
    # if not pais:
    #     pais = busca_dado(jsonData=location_opencage, dado='country')

    # dataFrame['rua'] = rua
    # dataFrame['numero'] = numero
    # dataFrame['bairro'] = bairro
    # dataFrame['cidade'] = cidade
    # dataFrame['estado'] = estado
    # dataFrame['cep'] = cep
    # dataFrame['pais'] = pais



    # for item in location:
    #     print(item.address)
    # base = "https://maps.googleapis.com/maps/api/geocode/json?"
    # # # &result_type=street_address
    # params = "latlng={lat},{lon}&language=pt-BR&key={key}".format(
    #     lat=latitude,
    #     lon=longitude,
    #     key=GOOGLE_MAPS_API_KEY
    # )
    # url = "{base}{params}".format(base=base, params=params)
    # print(url)
    # response = requests.get(url)
    # status = response.json()['status']
    # if status == 'OK':
    #     print('Tudo certo')
    #     print('\n')
    #     for valor in response.json()['results']:
    #         percorre_gmaps(valor)
    #     # print(response.json())
    #     # print('-------------\n')
    #     # separa_endereco(response=response.json()['results'], dataFrame=dataFrame)
    # else:
    #     print('Problemas')
    #     return status


#testeA['tipo'] = latitudes['tipo']
#testeA['graus'], testeA['decimal'] = latitudes['valores'].str.split('   ', 1).str

data = data.join(data['valores'].str.split('   ', 1, expand=True).rename(columns={0:'graus', 1:'decimal'}))

#data['valores_split'] = data['valores'].str.split('   ')
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
