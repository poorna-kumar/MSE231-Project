# repalce '2\r' with the category of interest
# output to file of interest
# only records categories that exist in that particular year
zcat index_m_yr2007.tsv.gz | grep $'2\r' | cut -d $'\t' -f 2 | uniq

