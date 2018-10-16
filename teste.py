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

data['valores_split'] = data['valores'].str.split('   ')
print(data.to_string().encode('utf-8').decode('latin-1'))
