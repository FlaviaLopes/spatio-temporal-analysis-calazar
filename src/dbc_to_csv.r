install.packages('read.dbc')
install.packages('list')
library(read.dbc)

dbc_to_csv <- function(input, output){
    input_path = sprintf('../data/%s', input)
    output_path = sprintf('../data/%s', output)
    files = list.files(input_path)
    files <- files[1:length(files)]
    for (i in 1:length(files)){
        df <- read.dbc(paste(input_path, '/', files[i], sep=''))
        write.csv(df, paste(output_path, '/', unlist(strsplit(files[i], '\\.'))[1], '.csv', sep=''))
    }
}
