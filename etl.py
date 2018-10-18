import pandas as pd
from variables import delimiter, input_columns, db_columns
from utils import busca_endereco
from sqlalchemy import create_engine
from pandas.io import sql
from decouple import config, Csv

def extract(source):
    return pd.read_csv(source, delimiter=delimiter, names=input_columns, header=None)

def transform(data):
    data = data.join(data['valores'].str.split('   ', 1, expand=True).rename(columns={0:'graus', 1:'decimal'}))
    latitudes = data[data['tipo'].str.contains('Latitude')]
    longitudes = data[data['tipo'].str.contains('Longitude')]
    distances = data[data['tipo'].str.contains('Distance')]
    latitudes = latitudes.reset_index()
    longitudes = longitudes.reset_index()
    distances = distances.reset_index()

    df = pd.DataFrame(columns=db_columns)
    df['LATITUDE'] = latitudes['decimal']
    df['LONGITUDE'] = longitudes['decimal']
    df['LATITUDEGRAUS'] = latitudes['graus']
    df['LONGITUDEGRAUS'] = longitudes['graus']
    df['DISTANCIA'] = distances['valores']
    df['BEARING'] = distances['bearing']

    df.apply(lambda coordenada: busca_endereco(coordenada), axis=1)
    return df

def load(data, destination):
    print(config('SQL_PASSWORD'))
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(user=config('SQL_USER', default='root'),
                                   pw=config('SQL_PASSWORD', default='root'),
                                   host=config('SQL_HOST', default='localhost'),
                                   db=config('DATAWAREHOUSE_DB')))
    data.to_sql(con=engine, name=config('DATAWAREHOUSE_NAME'), if_exists=config('IF_EXISTS', default='append'), index=config('SAVE_INDEX', default=False, cast=bool))

def etl(destination, source):
    data = pd.read_csv(source, delimiter=delimiter, names=input_columns, header=None)
    data = data.join(data['valores'].str.split('   ', 1, expand=True).rename(columns={0:'graus', 1:'decimal'}))
    latitudes = data[data['tipo'].str.contains('Latitude')]
    longitudes = data[data['tipo'].str.contains('Longitude')]
    distances = data[data['tipo'].str.contains('Distance')]
    latitudes = latitudes.reset_index()
    longitudes = longitudes.reset_index()
    distances = distances.reset_index()

    df = pd.DataFrame(columns=db_columns)
    df['LATITUDE'] = latitudes['decimal']
    df['LONGITUDE'] = longitudes['decimal']
    df['LATITUDEGRAUS'] = latitudes['graus']
    df['LONGITUDEGRAUS'] = longitudes['graus']
    df['DISTANCIA'] = distances['valores']
    df['BEARING'] = distances['bearing']

    df.apply(lambda coordenada: busca_endereco(coordenada), axis=1)
    print(df)

    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(user=config('SQL_USER', default='root'),
                                   pw=config('SQL_PASSWORD', default='root'),
                                   host=config('SQL_HOST', default='localhost'),
                                   db=config('DATAWAREHOUSE_DB')))
    df.to_sql(con=engine, name=config('DATAWAREHOUSE_NAME'), if_exists=config('IF_EXISTS', defualt='append'), index=config('SAVE_INDEX', default=False, cast=bool))
  # extract data from source db
  # source_cursor = source_cnx.cursor()
  # source_cursor.execute(query.extract_query)
  # data = source_cursor.fetchall()
  # source_cursor.close()
  #
  # # load data into warehouse db
  # if data:
  #   target_cursor = target_cnx.cursor()
  #   target_cursor.execute("USE {}".format(datawarehouse_name))
  #   target_cursor.executemany(query.load_query, data)
  #   print('data loaded to warehouse db')
  #   target_cursor.close()
  # else:
  #   print('data is empty')

def etl_process(destination, sources):
    print(sources)
    for arquivo in sources:
        data = extract(arquivo)
        data = transform(data)
        load(data=data, destination=destination)
        # etl(destination=destination, source=arquivo)


  #   if db_platform == 'mysql':
  #   source_cnx = mysql.connector.connect(**source_db_config)
  # elif db_platform == 'sqlserver':
  #   source_cnx = pyodbc.connect(**source_db_config)
  # elif db_platform == 'firebird':
  #   source_cnx = fdb.connect(**source_db_config)
  # else:
  #   return 'Error! unrecognised db platform'
  #
  # # loop through sql queries
  # for query in queries:
  #   etl(query, source_cnx, target_cnx)
  #
  # # close the source db connection
  # source_cnx.close()
