def main():
    print('iniciando etl')

if __name__ == "__main__":
    main()


# a base de dados salvara todos os dados, porem a query de extract so usara
# os dados pedidos no teste. O pandas le os arquivos e salva tudo no BD da
# warehouse, que depois faz o extract so dos dados necessarios.
# link: https://codeburst.io/using-python-script-for-data-etl-53138c567906
