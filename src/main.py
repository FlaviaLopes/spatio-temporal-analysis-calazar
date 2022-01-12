import datetime

import src.selecao as selecao
import src.limpeza as limpeza
import src.codificacao as codificacao
import src.enriquecimento as enriquecimento
import time


def etapa_selecao_1():
    selecao.convert_dbc_to_csv('raw/leivis', 'interim/leivis')
    selecao.convert_dbf_to_csv('raw/populacao', 'interim/populacao')
    selecao.concatenate_csv('interim/leivis', 'interim/leivis')
    selecao.concatenate_csv('interim/populacao', 'interim/populacao')


def etapa_limpeza():
    limpeza.update_leivis_columns_names(
        'interim/leivis/interim_leivis.csv',
        'interim/leivis/interim_leivis.csv'
    )
    limpeza.correct_leivis_co_uf(
        'interim/leivis/interim_leivis.csv',
        'interim/leivis/interim_leivis.csv'
    )
    limpeza.correct_leivis_dates(
        'interim/leivis/interim_leivis.csv',
        'interim/leivis/interim_leivis.csv'
    )
    limpeza.correct_leivis_weeks(
        'interim/leivis/interim_leivis.csv',
        'interim/leivis/interim_leivis.csv'
    )
    limpeza.correct_populacao_co_municipalities(
        'interim/populacao/interim_populacao.csv',
        'interim/populacao/interim_populacao.csv'
    )
    limpeza.correct_brasil_municipios_co_municipalities(
        'raw/municipios/brasil_municipios.xls',
        'interim/municipios/brasil_municipios.csv'
    )
    limpeza.correct_poligonos_municipalities(
        'raw/poligonos/BR_Municipios_2020.shp',
        'interim/poligonos/shapes.shp'
    )


def etapa_codificacao():
    codificacao.convert_leivis_columns_data_types(
        'interim/leivis/interim_leivis.csv',
        'interim/leivis/interim_leivis.csv'
    )


def etapa_selecao_2():
    selecao.select_brasil_municipios('interim/municipios/brasil_municipios.csv')
    selecao.select_populacao('interim/populacao/interim_populacao.csv')
    selecao.select_leivis('interim/leivis/interim_leivis.csv')
    selecao.select_poligonos('interim/poligonos/shapes.shp', uf='15')
    selecao.create_satscan_cases_file(
        'processed/cases_per_year_groupby_municipalities_all.csv',
        'processed/satscan/cases.csv',
        uf='15'
    )
    selecao.create_satscan_population_file(
        'interim/populacao/interim_populacao_reduced_all.csv',
        'processed/satscan/population.csv',
        uf='15'
    )
    selecao.create_satscan_grid_file(
        'raw/poligonos/BR_Localidades_2010_v1.shp',
        'processed/satscan/grid.csv',
        uf='15'
    )


def etapa_enriquecimento():
    enriquecimento.create_leivis_age_column(
        'interim/leivis/interim_leivis_reduced_all.csv',
        'interim/leivis/interim_leivis_reduced_all.csv'
    )
    enriquecimento.cases_per_year_groupby_municipalities(
        'interim/leivis/interim_leivis_reduced_all.csv',
        'interim/municipios/brasil_municipios_reduced_all.csv',
        'processed/cases_per_year_groupby_municipalities_all.csv'
    )
    enriquecimento.rates_per_year_groupby_municipalities(
        'processed/cases_per_year_groupby_municipalities_all.csv',
        'interim/populacao/interim_populacao_reduced_all.csv',
        'processed/rates_per_year_groupby_municipalities_all.csv'
    )


def pipeline():
    now = datetime.datetime.now()
    print(f'✅ Pipeline Iniciado em {now.hour}:{now.minute}:{now.second}')

    start = time.time()
    #etapa_selecao_1()
    print(f'✅ Etapa Seleção - Conversão, Integração: {round(time.time() - start, 2)} segundos')

    now = time.time()
    etapa_limpeza()
    print(f'✅ Etapa Limpeza: {round(time.time() - now, 2)} segundos')

    now = time.time()
    etapa_codificacao()
    print(f'✅ Etapa Codificação: {round(time.time() - now, 2)} segundos')

    now = time.time()
    etapa_selecao_2()
    print(f'✅ Etapa Seleção - Redução: {round(time.time() - now, 2)} segundos')

    now = time.time()
    etapa_enriquecimento()
    print(f'✅ Etapa Enriquecimento: {round(time.time() - now, 2)} segundos')

    print(f'✅ Pipeline Concluído.\nTempo total {round((time.time() - start) / 60, 2)} minutos')


if __name__:
    pipeline()
