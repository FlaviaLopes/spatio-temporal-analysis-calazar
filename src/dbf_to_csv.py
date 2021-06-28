#Converte arquivos de estimativa populacional em .dbf para .csv
from dbfread import DBF
import pandas as pd
import os

#Lê os arquivos no diretório de dados brutos, raw/populacao
#Itera cada arquivo .dbf lendo-o em dataframe pandas e salvando-o em seguida em .csv no diretório interim/populacao

pop_input_path = '../data/raw/populacao'
pop_output_path = '../data/interim/populacao'

dbf_files = [it for it in os.listdir(pop_input_path) if '.dbf' in it.lower()]

for file in dbf_files:
    dbf = DBF(f'{pop_input_path}/{file}')
    df_pop = pd.DataFrame(dbf)
    df_pop.to_csv(f'{pop_output_path}/{file.split(".")[0]}.csv', index=False)
