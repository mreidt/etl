import pandas as pd


data = pd.read_csv('data_points_20180101.txt', delimiter=':|  Bearing:', names=['tipo', 'valores', 'Bearing'], header=None)

latitudes = data[data['tipo'].str.contains('Latitude')]
longitudes = data[data['tipo'].str.contains('Longitude')]
distances = data[data['tipo'].str.contains('Distance')]
print(latitudes.to_string().encode('utf-8').decode('latin-1'))
print(longitudes.to_string().encode('utf-8').decode('latin-1'))
print(distances.to_string().encode('utf-8').decode('latin-1'))

#testeA['tipo'] = latitudes['tipo']
#testeA['graus'], testeA['decimal'] = latitudes['valores'].str.split('   ', 1).str

data = data.join(data['valores'].str.split('   ', 1, expand=True).rename(columns={0:'graus', 1:'decimal'}))

#data['valores_split'] = data['valores'].str.split('   ')
print(data.to_string().encode('utf-8').decode('latin-1'))

colunas = ['latitude', 'longitude', 'rua', 'numero', 'bairro', 'cidade', 'cep', 'estado', 'pais']
df = pd.DataFrame(columns=colunas)
df['latitude'] = data['decimal']
df['longitude'] = 

print(df)
