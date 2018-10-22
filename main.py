from etl import etl_process
from decouple import config, Csv

def main():
    etl_process(sources=config('INPUT_FILES', cast=Csv()))

if __name__ == "__main__":
    main()
