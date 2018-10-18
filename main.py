from etl import etl, etl_process
from decouple import config, Csv

def main():
    print('iniciando etl')
    etl_process(destination='123', sources=config('INPUT_FILES', cast=Csv()))

if __name__ == "__main__":
    main()


# a base de dados salvara todos os dados, porem a query de extract so usara
# os dados pedidos no teste. O pandas le os arquivos e salva tudo no BD da
# warehouse, que depois faz o extract so dos dados necessarios.
# link: https://codeburst.io/using-python-script-for-data-etl-53138c567906
# http://ryrobes.com/featured-articles/using-a-simple-python-script-for-end-to-end-data-transformation-and-etl-part-1/
# https://medium.com/@rchang/a-beginners-guide-to-data-engineering-part-i-4227c5c457d7
# https://blog.treasuredata.com/blog/2016/03/15/self-study-list-for-data-engineers-and-aspiring-data-architects/
