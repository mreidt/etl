from variables import datawarehouse_name
from decouple import config, Csv

datawarehouse_db_config = {
  'Trusted_Connection': 'yes',
  'driver': '{SQL Server}',
  'server': 'datawarehouse_sql_server',
  'database': config('DATAWAREHOUSE_NAME')
  'user': config('DB_USER', default='root'),
  'password': config('DB_PASSWORD', default='root'),
  'autocommit': True,
}

mysql_db_config = [
  {
    'user': config('SQL_USER', default='root'),
    'password': config('SQL_PASSWORD', default='root'),
    'host': 'db_connection_string_1',
    'database': config('SQL_DATABASE'),
  },
]

arquivos_origem = [
  {
    'name': config('INPUT_FILES')
  }
]
