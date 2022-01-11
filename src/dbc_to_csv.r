install.packages('read.dbc')
install.packages('list')
library(read.dbc)
input_path_leivis = '../data/raw/leivis'
output_path_leivis = '../data/interim/leivis'

#Lê os arquivos no diretório de dados brutos, raw/leivis
#Itera cada arquivo .dbc lendo-o em dataframe R e salvando-o em seguida em .csv no diretório interim/leivis

files = list.files(input_path_leivis)
files <- files[1:length(files)-1]
for (i in 1:length(files)){
    df <- read.dbc(paste(input_path_leivis, '/', files[i], sep=''))
    write.csv(df, paste(output_path_leivis, '/', unlist(strsplit(files[i], '\\.'))[1], '.csv', sep=''))
}

#- [READ.DBC - UM PACOTE PARA IMPORTAÇÃO DE DADOS DO DATASUS NA LINGUAGEM R] (https://docs.bvsalud.org/biblioref/2018/07/906543/anais_cbis_2016_artigos_completos-601-606.pdf)
