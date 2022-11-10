from pandas import DataFrame,read_excel
import psycopg2 as psycopg2
from os import remove,system
from datetime import datetime

try:
    conexao = psycopg2.connect()
    cursor = conexao.cursor()

    df = read_excel("posto_vaver.xlsx", engine='openpyxl')
    contador = int(len(df['EAN']))

    def dados():
        i = 0
        resultado = []
        while i < contador:
            try:
                comando = f"select * from backup.consulta_precos where codigobarras = lpad({df['EAN'][i]},13,0)"
                cursor.execute(comando)
                resultado.append(cursor.fetchall()[0])
                i += 1
            except:
                print("O produto ", df['EAN'][i]," informado esta errado valide com a loja" )
                i += 1
        return resultado

    def gerador():

        dia = datetime.now().strftime('%Y-%m-%d')
        new_df = DataFrame(data=dados())
        new_df.to_excel(f'Produtos&Updates--{dia}.xlsx',index=False,header=['Valor','EAN','Descrição','Update'])
        remove('posto_VAVER.xlsx')
        print("Arquivo gerado com sucesso")


    gerador()
    system('pause')
except:
    print('O arquivo não se encontra na pasta ou nome do arquivo esta incorreto')
    print('O deve estar no formato xlsx com o nome posto_vaver.xlsx ')
    system('pause')