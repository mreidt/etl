import pandas as pd
import requests


data = pd.read_csv('data_points_20180101.txt', delimiter=':|  Bearing:', names=['tipo', 'valores', 'bearing'], header=None)

GOOGLE_MAPS_API_KEY = 'AIzaSyCeWfCykKZLpMrg83oDcRoto_Aw4mHsyZM'

def separa_endereco(response, dataFrame):
    # R. Monsenhor Veras, 405 - Santana, Porto Alegre - RS, 90610-010, Brazil
    # TODO: verificar casos em que nao recebe o endereco completo
    for r in response:
        print(r)
        print('\n')
    # print(response)
    rua, numBairro, cidadeUf, cep, pais = response.split(',')
    numero, bairro = numBairro.split('-')
    cidade, uf = cidadeUf.split('-')

    dataFrame['rua']=rua
    dataFrame['numero']=numero
    dataFrame['bairro']=bairro
    dataFrame['cidade']=cidade
    dataFrame['estado']=uf
    dataFrame['cep']=cep
    dataFrame['pais']=pais

    print('--------------------\n')
    # return rua.strip(), numero.strip(), bairro.strip(), cidade.strip(), uf.strip(), cep.strip(), pais.strip()

def busca_endereco(dataFrame):
    latitude=dataFrame['latitude']
    longitude=dataFrame['longitude']
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&key={key}".format(
        lat=latitude,
        lon=longitude,
        key=GOOGLE_MAPS_API_KEY
    )
    url = "{base}{params}".format(base=base, params=params)
    print(url)
    response = requests.get(url)
    status = response.json()['status']
    if status == 'OK':
        print('Tudo certo')
        separa_endereco(response=response.json()['results'], dataFrame=dataFrame)
    else:
        print('Problemas')
        return status
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
