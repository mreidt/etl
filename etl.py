import pandas as pd
import os
from log import get_logger
from variables import delimiter, input_columns, db_columns
from utils import busca_endereco, fileType
from sqlalchemy import create_engine
from pandas.io import sql
from decouple import config, Csv
from exceptions import NotAType, NoInputFiles

logger = get_logger('logger')

def extract(source):
    if os.path.isfile(source):
        if fileType(source) == config('TAR_GZ_EXTENSION'):
            return pd.read_csv(source, delimiter=delimiter, compression='gzip',
                               names=input_columns, header=None
                              )
        elif fileType(source) == config('TXT_EXTENSION'):
            return pd.read_csv(source, delimiter=delimiter, names=input_columns,
                               header=None
                              )
        else:
            raise NotAType('{extension} is not a valid extension!'.format(extension=fileType(source)))
    else:
        raise FileNotFoundError('File {filename} not found!'.format(filename=source))

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

def load(data):
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(user=config('SQL_USER', default='root'),
                                   pw=config('SQL_PASSWORD', default='root'),
                                   host=config('SQL_HOST', default='localhost'),
                                   db=config('DATAWAREHOUSE_DB')))
    data.to_sql(con=engine, name=config('DATAWAREHOUSE_NAME'),
                if_exists=config('IF_EXISTS', default='append'),
                index=config('SAVE_INDEX', default=False, cast=bool))

def etlProcess(sources):
    try:
        if len(sources) == 0:
            raise NoInputFiles('Please, edit the .env file and provide some input files.')
    except TypeError:
        raise TypeError(TypeError)

    for arquivo in sources:
        logger.info('Processing file: {filename}'.format(filename=arquivo))
        data = extract(arquivo)
        data = transform(data)
        load(data=data)
        logger.info('{filename} done!'.format(filename=arquivo))

    return True
