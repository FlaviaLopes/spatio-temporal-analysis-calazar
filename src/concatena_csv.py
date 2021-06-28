import pandas as pd
import os

path_leivis = '../data/interim/leivis'
path_populacao = '../data/interim/populacao'

def concat_data(path):
    '''
    Lê todos arquivos no diretório passado (path) e os une em apenas um dataframe.
    Em seguida remove os arquivos do diretório em que foram unidos.
    output: salva um arquivo .csv no mesmo diretório de entrada fornecido.
    '''
    import os, errno
    def silent_remove(file):
        try:
            os.remove(file)
        except OSError as e:
            if e.errno != errno.ENOENT: 
                raise
    #agrupando bases - todos anos
    files = os.listdir(path)
    files = [it for it in files if '.csv' in it]
    df = pd.DataFrame()
    for filename in files:
        df = pd.concat([df, pd.read_csv(f'{path}/{filename}', encoding ='latin1', low_memory=False)], axis=0)

    df.to_csv(f"{path}/interim_{path.split('/')[-1]}.csv", index=False)
    
    for filename in files:
        silent_remove(f'{path}/{filename}')

concat_data(path_leivis)
concat_data(path_populacao)
