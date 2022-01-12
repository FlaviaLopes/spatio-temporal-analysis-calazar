import pandas as pd
import numpy as np


def convert_leivis_columns_data_types(input, output):
    """
    Etapa: Codificação
    Operação: Conversão de tipos (string para integer e datetime).
    :param input:
    :param output:
    :return:
    """
    data = pd.read_csv(f'../data/{input}')
    dates_columns = [
        'TRATAMENTO',
        'DT_NOT',
        'DT_PRI_SIN',
        'DT_NASC',
        'DT_INVEST',
        'DT_OBITO',
        'DT_ENCERRAMENTO',
        'DT_DESLC1',
        'DT_DESLC2',
        'DT_DESLC3'
    ]
    to_int_columns = ['ANO', 'CO_MN_INF', 'CO_MN_RESI', 'CO_MN_NOT', 'CS_GESTANT', 'CS_RACA',
                      'ID_OCUPA_N', 'CS_ESCOL_N', 'CO_PAIS', 'FEBRE', 'FRAQUEZA',
                      'EDEMA', 'EMAGRECIMENTO', 'DROGA', 'EVOLUCAO', 'DOENCA_TRABALHO',
                      'FALENCIA', 'TOSSE', 'PALIDEZ', 'BACO', 'INFECCIOSO', 'FEN_HEMORR',
                      'FIGADO', 'ICTERICIA', 'OUTROS', 'HIV', 'DIAG_PARASITOLOGICO',
                      'IFI', 'OUTRO', 'ENTRADA', 'DOSE', 'AMPOLAS', 'CRITERIO',
                      'TPAUTOCTO', 'CO_UF_INF', 'DS_MUN_1', 'CO_UF_1', 'CO_PAIS_1',
                      'DS_MUN_2', 'CO_UF_2', 'CO_PAIS_2', 'DS_MUN_3', 'CO_UF_3',
                      'CO_PAIS_3']

    data[to_int_columns] = data[to_int_columns].astype(np.float).astype("Int32")
    data[dates_columns] = data[dates_columns].apply(lambda x: pd.to_datetime(x), axis=1)
    data.to_csv(f'../data/{output}', index=False, encoding='utf-8')
