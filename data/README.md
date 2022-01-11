
# Sobre os dados


    ├── raw         - neste diretório ficam os dados originais, brutos, obtidos diretamente do site do datasus  e IBGE. Formatos .dbc, .dbf, .xls, .shp.
    |
    ├── interim     - neste diretório ficam os dados intermediários, que já passaram por um processamento, mas ainda não foi finalizado. Conversão de .dbc para .csv.
    |
    ├── processed   - neste diretório ficam os dados com processamento finalizado, pronto para serem utilizados nas análises.

## Instruções

### Base de dados finais do SINAN para LV
> Clique em [Serviços ->> Transferência/Download de arquivos ->> Sinan - Dados Finais](http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1&acao=41) 
> Na página de consulta selecione:
> - na primeira caixa: `Dados`
> - na segunda caixa: `Leishmaniose Visceral`
> - na terceira caixa: todos os anos
> - na quarta caixa: todos os estados
> Envie a consulta e em seguida selecione todos arquivos, dê um nome ao conjunto e faça o download.
> Salve o arquivo compactado no diretório `raw/leivis`, em seguida descompacte-o
> Obs.: Se vier arquivos faltante de algum estado faça o download separado por estado.
> Os que faltaram pra mim foram: PA, SC e RR.

### Base de estimativa populacional dos municípios
> Clique em [Serviços ->> Transferência/Download de arquivos ->> Bases Populacionais](http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1&acao=35&pad=31655) 
> Na página de consulta selecione:
> - na primeira caixa: `Bases Populacionais`
> - na segunda caixa: `Estimativas TCU - 1992 até 2019`
> - na terceira caixa: todos os anos
> - na quarta caixa: `BR`
> Envie a consulta e em seguida selecione todos arquivos, dê um nome ao conjunto e faça o download.
> Salve o arquivo compactado no diretório `raw/populacao`, em seguida descompacte-o e os demais arquivos compactados que existirem aninhados. Deixe no diretório apenas os .dbf de 2007 a 2019.

### Informações de municípios: código, microrregião, macrorregião, estado
> Acesse Informações de Municípios em ftp://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/divisao_territorial/2018/DTB_2018.zip 
> Salve o arquivo no diretório `raw/`, em seguida descompacte-o. Apenas arquivo `RELATORIO_DTB_BRASIL_MUNICIPIO.xls`. Outros oferecem informações de distritos e subdistritos de cada município, entretanto será desnecessário, visto que não há estimativas populacionais a nível distrital para cálculo de indicadores.

### Polígonos de área dos municípios brasileiros (visualização de mapas)
> Clique em [baixar polígonos](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2020/Brasil/BR/BR_Municipios_2020.zip)
> Salve o arquivo no diretório `raw/`, em seguida descompacte-o. Apenas .dbf, .shx e .shp.
