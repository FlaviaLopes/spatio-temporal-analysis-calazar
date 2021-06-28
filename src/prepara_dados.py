import pandas as pd
import numpy as np

def fix_co_uf(uf):  
    '''
    Todo código de município se inicia com o código da UF. 
    Esta função verifica se o campo uf (residência, infecção e notificação) está
    de acordo com o código do município e corrige.
    '''
    c_resi = (df.CO_MN_RESI.astype('string').str.startswith(str(uf)) & (df.CO_UF_RESI != uf))
    c_not = (df.CO_MN_NOT.astype('string').str.startswith(str(uf)) & (df.CO_UF_NOT != uf))
    c_inf = (df.CO_MN_INF.astype('string').str.startswith(str(uf)) & (df.CO_UF_INF != uf))
    
    if df.loc[c_resi, :].shape[0] > 0:
        df.loc[c_resi, 'CO_UF_RESI'] = uf
        
    if df.loc[c_not, :].shape[0] > 0:
        df.loc[c_not, 'CO_UF_NOT'] = uf
        
    if df.loc[c_inf, :].shape[0] > 0:
        df.loc[c_inf, 'CO_UF_INF'] = uf  

path_leivis = '../data/interim/leivis'
df = pd.read_csv(f'{path_leivis}/interim_leivis.csv', low_memory=False).drop('Unnamed: 0', axis=1)

#prepara dados de estimativas populacionais e exporta csv para /processed
path_populacao = '../data/interim/populacao/interim_populacao.csv'
populacao = pd.read_csv(path_populacao)
populacao.MUNIC_RES = populacao.MUNIC_RES.apply(lambda x: int(str(x)[:6]))
populacao = pd.pivot_table(populacao, values='POPULACAO', index='MUNIC_RES', columns='ANO')
populacao.reset_index().to_csv('../data/processed/processed_populacao.csv', index=False)

#prepara dados de municípios e exporta csv para /processed
path_municipios = '../data/raw/RELATORIO_DTB_BRASIL_MUNICIPIO.xls'
municipios = pd.read_excel(path_municipios)
municipios = municipios.loc[:, ['Código Município Completo','Nome_Município', 'Nome_UF', 'Nome_Mesorregião', 'Nome_Microrregião']]
municipios.columns = ['ibge_code', 'municipio','estado','mesorregiao','microrregiao']
municipios.ibge_code = municipios.ibge_code.apply(lambda x: str(x)[:6])
municipios.to_csv('../data/processed/processed_municipios.csv', index=False, encoding='utf-8')

#prepara, limpa e transforma, dados de notificações e exporta csv para /interim/leivis
path_leivis = '../data/interim/leivis'
df = pd.read_csv(f'{path_leivis}/interim_leivis.csv', low_memory=False).drop('Unnamed: 0', axis=1)

# renomeia colunas
df.columns = [
	'TP_NOT', 'ID_AGRAVO', 'DT_NOT', 'SEMANA_NOT', 'ANO', 'CO_UF_NOT',
    'CO_MN_NOT', 'ID_REGIONA', 'DT_PRI_SIN', 'SEMANA_PRI_SIN', 'DT_NASC',
	'NU_IDADE_N', 'CS_SEXO', 'CS_GESTANT', 'CS_RACA', 'CS_ESCOL_N', 'CO_UF_RESI',
	'CO_MN_RESI', 'ID_RG_RESI', 'CO_PAIS', 'NDUPLIC_N', 'CS_FLXRET',
	'FLXRECEBI', 'MIGRADO_W', 'DT_INVEST', 'ID_OCUPA_N', 'FEBRE',
	'FRAQUEZA', 'EDEMA', 'EMAGRECIMENTO', 'TOSSE', 'PALIDEZ', 'BACO', 'INFECCIOSO',
	'FEN_HEMORR', 'FIGADO', 'ICTERICIA', 'OUTROS', 'OUTROS_ESP', 'HIV',
	'DIAG_PARASITOLOGICO', 'IFI', 'OUTRO', 'ENTRADA', 'TRATAMENTO', 'DROGA', 'PESO',
	'DOSE', 'AMPOLAS', 'FALENCIA', 'CLASSI_FIN', 'CRITERIO', 'TPAUTOCTO',
	'CO_UF_INF', 'CO_PAIS_INF', 'CO_MN_INF', 'DOENCA_TRABALHO', 'EVOLUCAO',
	'DT_OBITO', 'DT_ENCERRAMENTO', 'DT_DESLC1', 'DS_MUN_1', 'CO_UF_1',
	'CO_PAIS_1', 'DS_TRANS_1', 'DT_DESLC2', 'DS_MUN_2', 'CO_UF_2',
	'CO_PAIS_2', 'DS_TRANS_2', 'DT_DESLC3', 'DS_MUN_3', 'CO_UF_3',
	'CO_PAIS_3', 'DS_TRANS_3'
]

#itera sobre as UFs da base corrigindo campos com a função fix_co_uf
for it in set(
	np.concatenate((
		df.CO_UF_INF.dropna().unique(),
   		df.CO_UF_RESI.dropna().unique(),
    	df.CO_UF_NOT.dropna().unique()
    ))
):
	fix_co_uf(int(it))

#remove 43 duplicações
df.drop(df.loc[df.NDUPLIC_N == 2, :].index, axis=0, inplace=True)

#Estes são casos registrados em municípios que hoje pertencem a Tocantins,
#mas estão com o código de UF antigo (52 Goiás). O restante do código continua o mesmo, somente substitui 52 por 17.
transferidos = pd.read_csv('../data/raw/transferidos_go-to.csv')
transferidos.columns = ['ibge_code','municipio']
transferidos = transferidos.set_index('ibge_code').to_dict()['municipio']
idx = df.loc[(~df.CO_MN_INF.map(transferidos).isnull()), :].index
df.loc[idx, 'CO_MN_INF'] = df.loc[idx, 'CO_MN_INF'].astype(int).astype('string').str.replace('52', '17')
df.loc[idx, 'CO_UF_INF'] = 17

#substitui data inválidas por np.nan
datas = ['TRATAMENTO','DT_NOT', 'DT_PRI_SIN', 'DT_NASC', 'DT_INVEST', 'DT_OBITO', 'DT_ENCERRAMENTO', 'DT_DESLC1', 'DT_DESLC2', 'DT_DESLC3']
locs = {}
for col in datas:
    if ((df[col].astype('string').str.len() < 10) & (~df[col].astype('string').str.contains('<NA>'))).any():
        idx = df.loc[df[col].astype('string').str.len() < 10, :].index.values.tolist()
        for i in idx:
            locs.update({i: col})

if locs:
    for k,v in locs.items():
        df.loc[k, v] = np.nan

#converte datas para tipo datetime: importante para cálculos
df[datas] = df[datas].apply(lambda x: pd.to_datetime(x), axis=1)

#algumas semanas epidemiológicas estão incompletas, fora do padrão AAAAss
df.loc[
    (df.SEMANA_NOT.astype('string').str.len() == 4), 'SEMANA_NOT'
] = '20' + df.loc[
    (df.SEMANA_NOT.astype('string').str.len() == 4), 'SEMANA_NOT'
].astype('string')
df.loc[
    (df.SEMANA_NOT.astype('string').str.len() == 3), 'SEMANA_NOT'
] = '200' + df.loc[
    (df.SEMANA_NOT.astype('string').str.len() == 3), 'SEMANA_NOT'
].astype('string')
df.loc[
    (df.SEMANA_PRI_SIN.astype('string').str.len() == 4), 'SEMANA_PRI_SIN'
] = '20' + df.loc[
    (df.SEMANA_PRI_SIN.astype('string').str.len() == 4), 'SEMANA_PRI_SIN'
].astype('string')
df.loc[
    (df.SEMANA_PRI_SIN.astype('string').str.len() == 3), 'SEMANA_PRI_SIN'
] = '200' + df.loc[
    (df.SEMANA_PRI_SIN.astype('string').str.len() == 3), 'SEMANA_PRI_SIN'
].astype('string')

#criando a coluna idade: idade da pessoa na data da notificação
df['IDADE'] = np.round( (df.DT_NOT - df.DT_NASC) / np.timedelta64('1', 'Y'), 6)

#algumas idades ficaram nulas pela falta de uma data ou outra, possivelmente a data de nascimento.
#Podemos extrair a idade do campo NU_IDADE_N, que é preenchido manualmente por quem faz a notificação, e preencher as amostras que ficaram sem IDADE
for index, row in df.loc[df.IDADE.isnull(), ['NU_IDADE_N', 'IDADE']].iterrows():
    if str(df.loc[index, 'NU_IDADE_N']).startswith('4'):
        df.loc[index, 'IDADE'] = int(str(df.loc[index, 'NU_IDADE_N'])[1:])
    if str(df.loc[index, 'NU_IDADE_N']).startswith('3'):
        df.loc[index, 'IDADE'] = np.round(int(str(df.loc[index, 'NU_IDADE_N'])[1:]) / 12, 6)
    if str(df.loc[index, 'NU_IDADE_N']).startswith('2'):
        df.loc[index, 'IDADE'] = np.round(int(str(df.loc[index, 'NU_IDADE_N'])[1:]) / 365, 6)
    if str(df.loc[index, 'NU_IDADE_N']).startswith('1'):
        df.loc[index, 'IDADE'] = 0

#convertendo colunas para tipo int, exceto peso e idade
cols = ['CS_GESTANT', 'CS_RACA', 'CS_ESCOL_N', 'CO_PAIS', 'FEBRE', 'FRAQUEZA',
       'EDEMA', 'EMAGRECIMENTO', 'TOSSE', 'PALIDEZ', 'BACO', 'INFECCIOSO',
       'FEN_HEMORR', 'FIGADO', 'ICTERICIA', 'OUTROS', 'HIV',
       'DIAG_PARASITOLOGICO', 'IFI', 'OUTRO', 'ENTRADA', 'DROGA', 'DOSE', 
       'AMPOLAS', 'FALENCIA', 'CRITERIO', 'TPAUTOCTO', 'CO_UF_INF',
       'DOENCA_TRABALHO', 'EVOLUCAO', 'DS_MUN_1', 'CO_UF_1', 'CO_PAIS_1',
       'DS_MUN_2', 'CO_UF_2', 'CO_PAIS_2', 'DS_MUN_3', 'CO_UF_3', 'CO_PAIS_3']

df[cols] = df[cols].astype(np.float).astype("Int32")

df = df.loc[df.CLASSI_FIN == 1, :].copy()

#excluindo colunas desnecessárias
df.drop(
    ['CS_FLXRET', 'FLXRECEBI', 'MIGRADO_W', 'NDUPLIC_N', 
     'TP_NOT', 'ID_REGIONA', 'ID_RG_RESI', 'ID_AGRAVO', 'CLASSI_FIN'
    ],
    axis=1,
    inplace=True
)

df.to_csv('../data/interim/leivis/interim_leivis_confirmados.csv',index=False)

#Não foram removidos CO_UF_INF e CO_MN_INF nulos
#Não foram removidos municípios ignorados
#Não foram removidos casos com entradas diferente de 1
#Foram descartados casos com CLASSI_FIN = 2, descartado.
#Não foram realizadas imputações/atualizações em CLASSI_FIN

