import datetime

import src.selecao as selecao
import src.limpeza as limpeza
import src.codificacao as codificacao
import src.enriquecimento as enriquecimento
import time


def etapa_selecao():
    selecao.convert_dbc_to_csv('raw/leivis', 'interim/leivis')
    selecao.convert_dbf_to_csv('raw/populacao', 'interim/populacao')
    selecao.concatenate_csv('interim/leivis', 'interim/leivis')
    selecao.concatenate_csv('interim/populacao', 'interim/populacao')
    selecao.select_brasil_municipios(
        'raw/municipios/brasil_municipios.xls',
        'interim/municipios/brasil_municipios_reduced.csv'
    )
    selecao.select_populacao(
        'interim/populacao/interim_populacao.csv',
        'interim/populacao/interim_populacao_reduced.csv'
    )
    selecao.select_leivis(
        'interim/leivis/interim_leivis.csv',
        'interim/leivis/interim_leivis_reduced.csv'
    )


def etapa_limpeza():
    limpeza.update_leivis_columns_names(
        'interim/leivis/interim_leivis_reduced.csv',
        'interim/leivis/interim_leivis_reduced.csv'
    )
    limpeza.correct_leivis_co_uf(
        'interim/leivis/interim_leivis_reduced.csv',
        'interim/leivis/interim_leivis_reduced.csv'
    )
    limpeza.correct_leivis_dates(
        'interim/leivis/interim_leivis_reduced.csv',
        'interim/leivis/interim_leivis_reduced.csv'
    )
    limpeza.correct_leivis_weeks(
        'interim/leivis/interim_leivis_reduced.csv',
        'interim/leivis/interim_leivis_reduced.csv'
    )
    limpeza.correct_populacao_co_municipalities(
        'interim/populacao/interim_populacao_reduced.csv',
        'interim/populacao/interim_populacao_reduced.csv'
    )
    limpeza.correct_brasil_municipios_co_municipalities(
        'interim/municipios/brasil_municipios_reduced.csv',
        'interim/municipios/brasil_municipios_reduced.csv'
    )


def etapa_codificacao():
    codificacao.convert_leivis_columns_data_types(
        'interim/leivis/interim_leivis_reduced.csv',
        'interim/leivis/interim_leivis_reduced.csv'
    )


def etapa_enriquecimento():
    enriquecimento.create_leivis_age_column(
        'interim/leivis/interim_leivis_reduced.csv',
        'interim/leivis/interim_leivis_reduced.csv'
    )
    enriquecimento.cases_per_year_groupby_municipalities(
        'interim/leivis/interim_leivis_reduced.csv',
        'interim/municipios/brasil_municipios_reduced.csv',
        'processed/cases_per_year_groupby_municipalities.csv'
    )
    enriquecimento.rates_per_year_groupby_municipalities(
        'processed/cases_per_year_groupby_municipalities.csv',
        'interim/populacao/interim_populacao_reduced.csv',
        'processed/rates_per_year_groupby_municipalities.csv'
    )


def pipeline():
    now = datetime.datetime.now()
    print(f'✅ Pipeline Iniciado em {now.hour}:{now.minute}:{now.second}')

    start = time.time()
    # etapa_selecao()
    # print(f'✅ Etapa Seleção: {round(time.time() - start, 2)} segundos')
    #
    # now = time.time()
    # etapa_limpeza()
    # print(f'✅ Etapa Limpeza: {round(time.time() - now, 2)} segundos')

    now = time.time()
    etapa_codificacao()
    print(f'✅ Etapa Codificação: {round(time.time() - now, 2)} segundos')

    now = time.time()
    etapa_enriquecimento()
    print(f'✅ Etapa Enriquecimento: {round(time.time() - now, 2)} segundos')

    print(f'✅ Pipeline Concluído.\nTempo total {round((time.time() - start) / 60, 2)} minutos')


if __name__:
    pipeline()
