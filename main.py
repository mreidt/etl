from etl import etlProcess
from decouple import config, Csv


def main():
    print('Starting ETL process')
    etlProcess(sources=config('INPUT_FILES', cast=Csv()))
    print('Ended ETL process')


if __name__ == "__main__":
    main()
