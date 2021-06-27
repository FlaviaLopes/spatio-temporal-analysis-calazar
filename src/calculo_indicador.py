import pandas as pd
import numpy as np

def total_casos_novos_municipio_infeccao_ano_14(df):
    '''
    | Importância do indicador: Conhecer a ocorrência de casos de LV, a distribuição espacial e temporal e
    | a tendência;
    |
    |Método de cálculo: Número total de casos novos de LV por local provável de infecção (UF, município, região administrativa ou localidade) no ano de notificação
    | input:
    | - df (dataframe com dados históricos)
    | - local (UF, município, região administrativa ou localidade)
    | - ano (2007 a 2019)
    | output:
    | - dataframe com Número total de casos novos de LV por local provável de infecção.
    | 
    |Indicador 14 do Caderno de Indicadores Leishmaniose Tegumentar Leishmaniose Visceral, 2018

    '''
    casos_novos = df.loc[
        (df.ENTRADA == 1) & 
        (~df.CO_MN_INF.isnull()) & 
        (~df.CO_MN_INF.astype('string').str.contains('0000')), 
        :
    ].copy()
    casos_novos.CO_MN_INF = casos_novos.CO_MN_INF.astype(int)
    mun = pd.read_csv('../data/processed/processed_municipios.csv').ibge_code.values
    anos = casos_novos['ANO'].unique()
    mun.sort()
    anos.sort()   
    
    casos_novos_por_ano = pd.DataFrame(index=mun)
    for ano in anos:
        casos_novos_por_ano = pd.concat([
            casos_novos_por_ano,
            casos_novos.loc[casos_novos.ANO == ano, :].groupby('CO_MN_INF')['CO_MN_INF'].count().rename(ano)
        ], axis=1)
    return casos_novos_por_ano.fillna(0)

   
def taxa_geral_incidencia_municipio_infeccao_ano_15(df):
    '''
    | Importância do indicador:
    | - Está relacionado à exposição de indivíduos à picada de fêmeas de flebotomíneos infectadas com
    | protozoários do gênero Leishmania;
    | - Identificar e monitorar no tempo o risco de ocorrência de casos de LV em determinada
    | população;
    | - Permite analisar as variações populacionais, geográficas e temporais na frequência de casos
    | confirmados de LV, como parte do conjunto de ações de vigilância epidemiológica e ambiental
    | da doença;
    | - Contribui para a avaliação e orientação das medidas de controle vetorial de flebotomíneos;
    | - Subsidia processos de planejamento, gestão e avaliação de políticas e ações de saúde
    | direcionadas ao controle da LV;
    | 
    | Limitações do indicador: Alguns casos do numerador não estarão contidos no denominador (casos
    | alóctones). 
    | 
    | Método de cálculo:
    | - Número total de casos novos de LV por local provável de infecção (município) 
    | no ano de notificação dividido por População total do município no
    | ano de notificação x 100.000
    |
    |Indicador 15 do Caderno de Indicadores Leishmaniose Tegumentar Leishmaniose Visceral, 2018
    '''
    taxa = total_casos_novos_municipio_infeccao_ano_14(df)
    pop = pd.read_csv('../data/processed/processed_populacao.csv').set_index('MUNIC_RES')
    pop.columns = pop.columns.astype(int)
    for idx in taxa.index:
        try:
            taxa.loc[idx] = taxa.loc[idx] / pop.loc[idx] * 100000
        except:
            print(idx)
    return taxa.fillna(0)


output = '../data/indicadores/visceral/{}'
confirmados = pd.read_csv('../data/interim/leivis/interim_leivis_confirmados.csv', low_memory=False)

total_casos_novos_municipio_infeccao_ano_14(
    confirmados
).reset_index().rename(
    columns={'index': 'CO_MN_INF'}
).fillna(0).to_csv(output.format('indicador_14_total_casos_novos_municipio_infeccao.csv'), index=False)

taxa_geral_incidencia_municipio_infeccao_ano_15(
    confirmados
).reset_index().rename(
    columns={'index': 'CO_MN_INF'}
).fillna(0).to_csv(output.format('indicador_15_taxa_incidencia_municipio_infeccao.csv'), index=False)