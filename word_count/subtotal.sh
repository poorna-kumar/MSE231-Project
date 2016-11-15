zcat wc_200701.out.gz | awk -F$'\t' '{m += $2; f +=$3} END {print m, f}'
