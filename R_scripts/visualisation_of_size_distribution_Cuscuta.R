data = read.table('/mnt/raid/users/tihana/200226_CEUR/lastz_ref_db_200226/pseudocoding_ref_db_200226/analysis/coded_table.length_table', stringsAsFactors = FALSE)

groups = c('rDNA_45S', 'rDNA_5S', 'Chromov', 'SAT_CUSTR65', 'SAT_CUSTR66', 'SAT_CUSTR67', 'LINE', 'nonChromov', 'SAT_CUSTR2', 'SAT_CUSTR24', 'SAT_CUSTR25', 'SIRE', 'SSR_TRA', 'TEL', 'Ty1_except_SIRE')

pdf('/mnt/raid/users/tihana/200226_CEUR/lastz_ref_db_200226/pseudocoding_ref_db_200226/analysis/coded_all.length.pdf')

for (i in groups) {
  intact_i = subset(data, V1==i&V5=='I')
  truncated_i = subset(data, V1==i&V5=='T')
  
  intact_name = paste('Length of intact ', i, sep='')
  intact_counts = as.vector(table(intact_i[,2]))
  intact_lengths = as.integer(names(table(intact_i[,2])))
  #print(intact_counts[800:1600])
  plot(x=intact_lengths, y=intact_counts, type='h', main=intact_name, xlab='length', ylab='frequency')

  truncated_name =  paste('Length of truncated ', i, sep='')
  truncated_counts = as.vector(table(truncated_i[,2]))
  truncated_lengths = as.integer(names(table(truncated_i[,2])))
  #plot(x=seq(1,length(truncated_counts)), y=truncated_counts, type='h', main=truncated_name, xlab='length', ylab='frequency')
  plot(x=truncated_lengths, y=truncated_counts, type='h', main=truncated_name, xlab='length', ylab='frequency')
  
}

dev.off()

#################################

data = read.table('/mnt/raid/users/tihana/200226_CEUR/lastz_ref_db_200226/pseudocoding_ref_db_200226/analysis/coded_table.length_table', stringsAsFactors = FALSE)
i = 'LINE'
intact_i = subset(data, V1==i&V5=='I')
intact_name = paste('Length of intact ', i, sep='')
intact_counts = as.vector(table(intact_i[,2]))
intact_lengths = as.integer(names(table(intact_i[,2])))
plot(x=intact_lengths, y=intact_counts, type='h', main=intact_name, xlab='length', ylab='frequency', xlim=c(1,7000))
a = sum(intact_counts[3:length(intact_counts)])
b = sum(intact_counts)
c = sum(intact_counts[1:2])
a/b
c/a
