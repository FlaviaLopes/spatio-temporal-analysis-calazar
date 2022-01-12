import pandas as pd
import numpy as np


def create_leivis_age_column(input_data, output):
    """
    Descrição: IDADE no dia da notificação "DT_NOT - DT_NASC".
    Se uma das datas estiver ausente, a idade é extraída do campo "NU_IDADE_N"
    Etapa: Enriquecimento
    Operação: Construção de atributos
    :param input_data:
    :param output:
    :return:
    """
    data = pd.read_csv(f'../data/{input_data}', parse_dates=['DT_NOT', 'DT_NASC'])
    data['IDADE'] = np.round((data.DT_NOT - data.DT_NASC) / np.timedelta64('1', 'Y'), 6)

    for index, row in data.loc[data.IDADE.isnull(), ['NU_IDADE_N', 'IDADE']].iterrows():
        if str(data.loc[index, 'NU_IDADE_N']).startswith('4'):
            data.loc[index, 'IDADE'] = int(str(data.loc[index, 'NU_IDADE_N'])[1:])
        if str(data.loc[index, 'NU_IDADE_N']).startswith('3'):
            data.loc[index, 'IDADE'] = np.round(int(str(data.loc[index, 'NU_IDADE_N'])[1:]) / 12, 6)
        if str(data.loc[index, 'NU_IDADE_N']).startswith('2'):
            data.loc[index, 'IDADE'] = np.round(int(str(data.loc[index, 'NU_IDADE_N'])[1:]) / 365, 6)
        if str(data.loc[index, 'NU_IDADE_N']).startswith('1'):
            data.loc[index, 'IDADE'] = 0

    data.to_csv(f'../data/{output}', index=False, encoding='utf-8')


def cases_per_year_groupby_municipalities(cases, municipalities, output):
    """
    Descrição:
    | Importância do indicador: Conhecer a ocorrência de casos de LVH, a distribuição espacial e temporal e a tendência;
    |
    | Método de cálculo: Número total de casos novos de LVH por local provável de infecção
    | (UF, município, região administrativa ou localidade) no ano de notificação
    |
    |Indicador 14 do Caderno de Indicadores Leishmaniose Tegumentar Leishmaniose Visceral, 2018
    :param cases: base de notificações
    :param municipalities: base de municípios
    :param output: dataframe com Número total de casos novos de LV por local provável de infecção.
    :return:
    """
    data = pd.read_csv(f'../data/{cases}')
    mun = pd.read_csv(f'../data/{municipalities}').ibge_code.values
    years = data['ANO'].unique()
    mun.sort()
    years.sort()

    new_cases_per_year = pd.DataFrame(index=mun)
    for year in years:
        new_cases_per_year = pd.concat([
            new_cases_per_year,
            data.loc[data.ANO == year, :].groupby('CO_MN_INF')['CO_MN_INF'].count().rename(year)
        ], axis=1)
    new_cases_per_year.fillna(0).rename_axis('ibge_code').reset_index().to_csv(f'../data/{output}', index=False)


def rates_per_year_groupby_municipalities(cases_per_year, population, output):
    """
    Descrição:
    | Importância do indicador: Está relacionado à exposição de indivíduos à picada de fêmeas de flebotomíneos
    | infectadas com protozoários do gênero Leishmania;    |
    | Identificar e monitorar no tempo o risco de ocorrência de casos de LV em determinada população;    |
    | Permite analisar as variações populacionais, geográficas e temporais na frequência de casos confirmados
    | de LV, como parte do conjunto de ações de vigilância epidemiológica e ambiental da doença;    |
    | Contribui para a avaliação e orientação das medidas de controle vetorial de flebotomíneos;    |
    | Subsidia processos de planejamento, gestão e avaliação de políticas e ações de saúde direcionadas
    | ao controle da LV;
    |
    | Limitações do indicador: Alguns casos do numerador não estarão contidos no denominador (casos
    | alóctones).
    |
    | Método de cálculo: Número total de casos novos de LV por local provável de infecção (município)
    | no ano de notificação dividido por População total do município no ano de notificação x 100.000
    |
    |Indicador 15 do Caderno de Indicadores Leishmaniose Tegumentar Leishmaniose Visceral, 2018
    :param cases_per_year: indicador total de casos por ano e municipio
    :param population: base de estimativa populacional
    :param output: indicador taxa de incidência.
    :return:
    """
    rates_per_year = pd.read_csv(f'../data/{cases_per_year}', index_col='ibge_code')
    pop = pd.read_csv(f'../data/{population}').set_index('MUNIC_RES')
    for idx in rates_per_year.index:
        rates_per_year.loc[idx] = rates_per_year.loc[idx] / pop.loc[idx] * 100000

    rates_per_year.fillna(0).to_csv(f'../data/{output}')
