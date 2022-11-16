import pandas as pd
import numpy as np


def update_leivis_columns_names(data_input, data_output):
    """
    Descrição: padronizar os nomes de colunas
    Etapa: Limpeza
    Operação: Não definida.
    :param data_input:
    :param data_output:
    :return:
    """
    new_cols = {
        'DT_NOTIFIC': 'DT_NOT',
        'SEM_NOT': 'SEMANA_NOT',
        'NU_ANO': 'ANO',
        'SG_UF_NOT': 'CO_UF_NOT',
        'ID_MUNICIP': 'CO_MN_NOT',
        'DT_SIN_PRI': 'DT_PRI_SIN',
        'SEM_PRI': 'SEMANA_PRI_SIN',
        'SG_UF': 'CO_UF_RESI',
        'ID_MN_RESI': 'CO_MN_RESI',
        'ID_PAIS': 'CO_PAIS',
        'EMAGRA': 'EMAGRECIMENTO',
        'DIAG_PAR_N': 'DIAG_PARASITOLOGICO',
        'COUFINF': 'CO_UF_INF',
        'COPAISINF': 'CO_PAIS_INF',
        'COMUNINF': 'CO_MN_INF',
        'DOENCA_TRA': 'DOENCA_TRABALHO',
        'DT_ENCERRA': 'DT_ENCERRAMENTO',
    }
    data = pd.read_csv(f'../data/{data_input}', low_memory=False)
    cols = pd.Series(data.columns)
    cols = list(cols.replace(new_cols))
    data.columns = cols
    data.to_csv(f'../data/{data_output}', index=False, encoding='utf-8')


def correct_leivis_co_uf(data_input, data_output):
    """
    Descrição:
    1) Inconsistência a ser corrigida: 2 primeiros dígitos do código do município têm que ser iguais ao respectivo
    código de UF: (CO_MN_RESI[:2] = CO_UF_RESI, CO_MN_INF[:2] = CO_UF_INF, CO_MN_NOT[:2] = CO_UF_NOT)
    2) Corrige municípios que eram de Goiás (52), mas são de Tocantins no período (17)
    Etapa: Limpeza
    Operação: Limpeza de inconsistências por correção de erros
    :param data_input:
    :param data_output:
    :return:
    """
    data = pd.read_csv(f'../data/{data_input}', low_memory=False)

    def iterate_co_uf(uf):
        c_resi = (data.CO_MN_RESI.astype('string').str.startswith(str(uf)) & (data.CO_UF_RESI != uf))
        c_not = (data.CO_MN_NOT.astype('string').str.startswith(str(uf)) & (data.CO_UF_NOT != uf))
        c_inf = (data.CO_MN_INF.astype('string').str.startswith(str(uf)) & (data.CO_UF_INF != uf))

        if data.loc[c_resi, :].shape[0] > 0:
            data.loc[c_resi, 'CO_UF_RESI'] = uf

        if data.loc[c_not, :].shape[0] > 0:
            data.loc[c_not, 'CO_UF_NOT'] = uf

        if data.loc[c_inf, :].shape[0] > 0:
            data.loc[c_inf, 'CO_UF_INF'] = uf

    ufs = set(
        np.concatenate(
            (data.CO_UF_INF.dropna().unique(), data.CO_UF_RESI.dropna().unique(), data.CO_UF_NOT.dropna().unique())
        )
    )
    for it in ufs:
        iterate_co_uf(int(it))

    # uma única inconsistência no atributo ID_OCUPA_N
    data.ID_OCUPA_N = data.ID_OCUPA_N.replace('XXX', np.nan, inplace=True)

    # corrige código de municípios que eram de GO e hj são de TO
    transferidos = pd.read_csv('../data/raw/municipios/transferidos_go-to.csv')
    transferidos.columns = ['ibge_code', 'municipio']
    transferidos = transferidos.set_index('ibge_code').to_dict()['municipio']
    idx = data.loc[(~data.CO_MN_INF.map(transferidos).isnull()), :].index
    if idx.any():
        data.loc[idx, 'CO_MN_INF'] = data.loc[idx, 'CO_MN_INF'].astype(int).astype('string').str.replace('52', '17')
        data.loc[idx, 'CO_UF_INF'] = 17
    data.to_csv(f'../data/{data_output}', index=False, encoding='utf-8')


def correct_leivis_dates(data_input, data_output):
    """
    Descrição: Inconsistência a ser corrigida: datas com formato inconsistente
    Objetivo: Converter data de string para datetime
    Etapa: Limpeza
    Operação: Limpeza de inconsistências por correção de erros e Conversão de tipo
    :param data_input:
    :param data_output:
    :return:
    """
    data = pd.read_csv(f'../data/{data_input}')
    dates_columns = [
        'TRATAMENTO',
        'DT_NOT',
        'DT_PRI_SIN',
        'DT_NASC',
        'DT_INVEST',
        'DT_OBITO',
        'DT_ENCERRAMENTO',
        'DT_DESLC1',
        'DT_DESLC2', 'DT_DESLC3'
    ]

    def look_for_invalid_date():
        locs = {}
        for col in dates_columns:
            if ((data[col].astype('string').str.len() < 10) & (~data[col].astype('string').str.contains('<NA>'))).any():
                idx = data.loc[data[col].astype('string').str.len() < 10, :].index.values.tolist()
                for i in idx:
                    locs.update({i: col})
        return locs

    while True:
        locs = look_for_invalid_date()
        if locs:
            for k, v in locs.items():
                print('_' * 50)
                print('Insira a data correta <aaaa-mm-dd>, ou insira 0')
                print(data.loc[k, v])
                value = input()
                if value == '0':
                    data.loc[k, v] = np.nan
                elif len(value) == 10:
                    data.loc[k, v] = value
                print('_' * 50)
        else:
            break

    data.to_csv(f'../data/{data_output}', index=False, encoding='utf-8')


def correct_leivis_weeks(data_input, data_output):
    """
    Descrição: algumas semanas epidemiológicas estão incompletas, fora do padrão AAAAss
    Etapa: Limpeza
    Operação: Limpeza de inconsistências por correção de erros
    TODO: em dados futuros pode não funcionar. A melhorar.
    :param data_input:
    :param data_output:
    :return:
    """
    data = pd.read_csv(f'../data/{data_input}')

    condition_one = data.SEMANA_NOT.astype('string').str.len() == 4
    data.loc[condition_one, 'SEMANA_NOT'] = '20' + data.loc[condition_one, 'SEMANA_NOT'].astype('string')

    condition_two = data.SEMANA_NOT.astype('string').str.len() == 3
    data.loc[condition_two, 'SEMANA_NOT'] = '200' + data.loc[condition_two, 'SEMANA_NOT'].astype('string')

    condition_three = data.SEMANA_PRI_SIN.astype('string').str.len() == 4
    data.loc[condition_three, 'SEMANA_PRI_SIN'] = '20' + data.loc[condition_three, 'SEMANA_PRI_SIN'].astype('string')

    condition_four = data.SEMANA_PRI_SIN.astype('string').str.len() == 3
    data.loc[condition_four, 'SEMANA_PRI_SIN'] = '200' + data.loc[condition_four, 'SEMANA_PRI_SIN'].astype('string')

    data.to_csv(f'../data/{data_output}', index=False, encoding='utf-8')


def correct_populacao_co_municipalities(data_input, data_output):
    """
    Etapa: Limpeza
    Operação: Limpeza de inconsistências por correção de erros
    :param data_input:
    :param data_output:
    :return:
    """
    data = pd.read_csv(f'../data/{data_input}')
    data.MUNIC_RES = data.MUNIC_RES.apply(lambda x: int(str(x)[:6]))
    data = pd.pivot_table(data, values='POPULACAO', index='MUNIC_RES', columns='ANO')
    data.reset_index().to_csv(f'../data/{data_output}', index=False)


def correct_brasil_municipios_co_municipalities(data_input, data_output):
    """
    Etapa: Limpeza
    Operação: Limpeza de inconsistências por correção de erros
    :param data_input:
    :param data_output:
    :return:
    """
    data = pd.read_excel(f'../data/{data_input}')
    data.columns = ['uf', 'estado', 'cod_mesorregiao', 'mesorregiao', 'cod_microrregiao', 'microrregiao',
                    'cod_municipio', 'ibge_code', 'municipio']
    data.ibge_code = data.ibge_code.apply(lambda x: str(x)[:6])
    data.to_csv(f'../data/{data_output}', index=False, encoding='utf-8')


def correct_poligonos_municipalities(data_input, data_output):
    """
    Etapa: Limpeza
    Operação: Limpeza de inconsistências por correção de erros
    :param data_input:
    :param data_output:
    :return:
    """
    import geopandas as gpd
    shapes = gpd.read_file(f'../data/{data_input}', encoding='utf-8')
    shapes.columns = ['ibge_code', 'municipio', 'co_uf', 'area_km2', 'geometry']
    shapes.ibge_code = shapes.ibge_code.apply(lambda x: x[0:6])
    shapes.ibge_code = shapes.ibge_code.astype(int)
    shapes.to_file(f'../data/{data_output}', encoding='utf-8', index=False)
