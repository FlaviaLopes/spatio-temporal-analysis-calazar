from dbfread import DBF
import rpy2.robjects as ro
import pandas as pd
import os


def convert_dbc_to_csv(input, output):
    """
    Descrição: Esta função executa o script em R usando rpy2.
    Etapa: Pré-Seleção
    Operação: Conversão de dados
    :param input:
    :param output:
    :return:
    """
    r = ro.r
    r.source('dbc_to_csv.r')
    r.dbc_to_csv(input, output)


def convert_dbf_to_csv(input, output):
    """
    Descrição: Converte os dados brutos de .dbf para .csv
    Etapa: Pré-Seleção
    Operação: Conversão de Dados
    :param input:
    :param output:
    :return:
    """
    input_path = f'../data/{input}'
    output_path = f'../data/{output}'
    dbf_files = [it for it in os.listdir(input_path) if '.dbf' in it.lower()]
    for file in dbf_files:
        dbf = DBF(f'{input_path}/{file}')
        df = pd.DataFrame(dbf)
        df.to_csv(f'{output_path}/{file.split(".")[0]}.csv', index=False)


def concatenate_csv(input, output, drop_original=True):
    """
    Descrição: Lê e junta todos arquivos .csv em um dataframe.
    Etapa: Pré-Seleção
    Operação: União de bases de dados
    :param input:
    :param output:
    :param drop_original: Se True, substitui os arquivos individuais por um único .csv
    :return:
    """
    import errno

    def silent_remove(file):
        try:
            os.remove(file)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    input_path = f'../data/{input}'
    output_path = f'../data/{output}'
    files = os.listdir(input_path)
    files = [it for it in files if '.csv' in it]
    df = pd.DataFrame()
    for filename in files:
        df = pd.concat([df, pd.read_csv(f'{input_path}/{filename}', encoding='latin1', low_memory=False)], axis=0)

    if drop_original:
        for filename in files:
            silent_remove(f'{input_path}/{filename}')
    df.to_csv(f"{output_path}/{output.replace('/', '_')}.csv", index=False)


def select_brasil_municipios(input, output):
    """
    Etapa: Seleção
    Operação: Redução de Dados Vertical e Horizontal Direta
    :param input:
    :param output:
    :param columns:
    :return:
    """
    path = f'../data/{input}'
    columns = ['Código Município Completo', 'Nome_Município', 'Nome_UF', 'Nome_Mesorregião', 'Nome_Microrregião']
    data = pd.read_excel(path)
    data = data.loc[
        data['Código Município Completo'].astype('string').str.startswith('15'),
        columns
    ].copy()
    data.to_csv(f"../data/{output}", index=False, encoding='utf-8')


def select_populacao(input, output):
    """
    Etapa: Seleção
    Operação: Redução de Dados Horizontal Direta
    :param path_name:
    :return:
    """
    data = pd.read_csv(f'../data/{input}', low_memory=False)
    data = data.loc[data.MUNIC_RES.astype('string').str.startswith('15'), :].copy()
    data.to_csv(f"../data/{output}", index=False, encoding='utf-8')


def select_leivis(input, output):
    """
    Etapa: Seleção
    Operação: Redução de Dados Vertical e Horizontal Direta
    :param input:
    :param output:
    :return:
    """
    data = pd.read_csv(f'../data/{input}', low_memory=False).drop('Unnamed: 0', axis=1)
    data = data.loc[
           (data.COMUNINF.astype('string').str.startswith('15') | (data.COUFINF.astype('string').str.startswith('15'))),
           :
           ].copy()
    data.drop(data.loc[data.NDUPLIC_N == 2, :].index, axis=0, inplace=True)
    data = data.loc[data.CLASSI_FIN == 1, :].copy()
    data = data.loc[data.ENTRADA == 1, :].copy()
    data = data.loc[~data.COMUNINF.isnull()].copy()
    data = data.loc[~data.COMUNINF.astype('string').str.contains('0000')].copy()

    data.drop([
        'CS_FLXRET', 'FLXRECEBI', 'MIGRADO_W', 'NDUPLIC_N', 'TP_NOT', 'ID_REGIONA', 'ID_RG_RESI', 'ID_AGRAVO',
        'CLASSI_FIN'
    ], axis=1, inplace=True
    )

    data.to_csv(f"../data/{output}", index=False, encoding='utf-8')


def select_poligonos(input, output):
    """
    Etapa: Seleção
    Operação: Redução de Dados Horizontal Direta
    :param input:
    :param output:
    :return:
    """
    import geopandas as gpd
    shapes = gpd.read_file(f'../data/{input}', encoding='utf-8')
    shapes.loc[shapes.SIGLA_UF == 'PA'].to_file(f'../data/{output}', index=False, encoding='utf-8')


def create_satscan_cases_file(input, output):
    """
    Descrição: O formato esperado para o arquivo de casos, usando o modelo Poisson de probabilidade, é:
    `<Location ID><Number of Cases><Date/Time><Covariate 1><Covariate N>`
    Etapa: Seleção
    Operação:
    :param input:
    :param output:
    :return:
    """
    cases = pd.read_csv(f'../data/{input}', index_col='ibge_code')
    satscan_cases = pd.DataFrame(columns=['ibge_code', 'cases', 'year'])
    for it in cases.index:
        aux = pd.DataFrame(columns=['ibge_code', 'cases', 'year'])
        aux.cases = cases.loc[it, :].astype('int')
        aux.year = cases.columns
        aux.ibge_code = it
        satscan_cases = pd.concat([satscan_cases, aux])
    satscan_cases = satscan_cases.reset_index().drop('index', axis=1)
    satscan_cases.to_csv(f'../data/{output}', index=False)


def create_satscan_population_file(input, output):
    """
    Descrição: O formato esperado do arquivo populacional é:
    <Location ID> <Date/Time> <Population> <Covariate 1> ... <Covariate N>
    Etapa: Seleção
    Operação:
    :param input:
    :param output:
    :return:
    """
    pop = pd.read_csv(f'../data/{input}', index_col='MUNIC_RES')
    idx_nan = pop.loc[pop.T.isnull().any(), :].index.values
    for it in idx_nan:
        pop.loc[it, :] = pop.loc[it, :].fillna(pop.loc[it, :].mean())

    satscan_pop = pd.DataFrame(columns=['ibge_code', 'year', 'population'])
    for it in pop.index:
        aux = pd.DataFrame(columns=['ibge_code', 'year', 'population'])
        aux.population = pop.loc[it, :]
        aux.year = pop.columns
        aux.ibge_code = it
        satscan_pop = pd.concat([satscan_pop, aux])
    satscan_pop = satscan_pop.reset_index().drop('index', axis=1)
    satscan_pop.to_csv(f'../data/{output}', index=False)


def create_satscan_grid_file(input, output):
    """
    Descrição: "O arquivo de grade opcional define os centróides dos círculos utilizados pela estatística de varredura.
    Se não for especificado nenhum arquivo de grade, as coordenadas dadas no arquivo de coordenadas serão usadas para esta finalidade."
    Existem no Pará municípios muito extensos. Se o arquivo de grade não for especificado o centro do município ficará
    como padrão e distante das regiões densamente habitadas (cidade), por exemplo Altamira. O arquivo de grade vai definir
    como centróide do município a cidade deste.
    O formato esperado é <latitude><longitude
    Etapa: Seleção
    Operação:
    :param input:
    :param output:
    :return:
    """
    import geopandas as gpd
    geo = gpd.read_file(f'../data/{input}', encoding='latin-1')
    geo.loc[
        (geo.NM_UF == 'PARÁ') &
        (geo.NM_CATEGOR == 'CIDADE') |
        (geo.NM_LOCALID == 'MUJUÍ DOS CAMPOS'),
        ['LAT', 'LONG']
    ].to_csv(f'../data/{output}', index=False)
