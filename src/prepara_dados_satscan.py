import pandas as pd
import geopandas as gpd


df = pd.read_csv('../data/indicadores/visceral/indicador_14_total_casos_novos_municipio_infeccao.csv')

#The expected format of the case file, using the Poisson probability model is:
#`<Location ID><Number of Cases><Date/Time><Covariate 1><Covariate N>`
casos = pd.DataFrame()
for it in df.columns[1:]:
    temp = df.loc[:, ['CO_MN_INF', it]].copy()
    temp.columns = ['location_id', 'cases']
    temp['time'] = it
    casos = pd.concat([casos, temp])
casos.cases = casos.cases.astype(int)
casos.to_csv('../data/processed/satscan_experiment_data/casos.csv', index=False)

#The expected format of the population file is:
#`<Location ID> <Date/Time> <Population> <Covariate 1> ... <Covariate N>`

df = pd.read_csv('../data/processed/processed_populacao.csv')

#há municípios sem informação populacional: preencher com 0
index = df.loc[df.T.isnull().any(), :].index
for it in index:
    df.iloc[it, :] = df.iloc[it, :].fillna(df.iloc[it, 1:].mean())
pop = pd.DataFrame()
for it in df.columns[1:]:
    temp = df.loc[:, ['MUNIC_RES', it]].copy()
    temp.columns = ['location_id', 'pop']    
    temp.insert(loc=1, column='time', value=it)
    pop = pd.concat([pop, temp])    
pop.to_csv('../data/processed/satscan_experiment_data/pop.csv', index=False)

#corrigir código município de 7 dígitos para 6 dígitos
geo = gpd.read_file('../data/raw/poligonos/BR_Municipios_2020.shp')
geo.CD_MUN = geo.CD_MUN.astype('string').str[0:6]
geo.to_file('../data/processed/satscan_experiment_data/geo')
