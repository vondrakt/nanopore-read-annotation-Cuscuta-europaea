#!/usr/bin/env R

args = commandArgs(trailingOnly=TRUE)
density = read.table(args[1], stringsAsFactors = FALSE)
png(args[2])

a = density[,1:389]
b = density[,390:778]
c = a+b

plot(x=seq(from=1, to=389), y=c, type = 'h', bty='n', main='Density profile', xlab = 'positions', ylab='density')
dev.off()

# density = read.table('/mnt/raid/users/tihana/200226_CEUR/lastz_ref_db_200226/pseudocoding_ref_db_200226/analysis/LINE_insertion_preference/CUSTR24_DIMER_vs_coded_all_G_window_200_200522_p70.density__5_end', stringsAsFactors = FALSE)
# a = density[,1:389]
# b = density[,390:778]
# c = a+b
# plot(x=seq(from=1, to=389), y=c, type = 'h', bty='n', main='Density profile', xlab = 'positions', ylab='density', xlim=c(210,212))
