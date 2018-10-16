import pandas as pd


data = pd.read_csv('data_points_20180101.txt', delimiter=':|  Bearing:', names=['tipo', 'valores', 'bearing'], header=None)



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

print(df)
