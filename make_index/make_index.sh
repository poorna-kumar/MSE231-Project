# exit if any part fails
set -e

# for 2007, there's only 6 months of data
for mo in `seq 1 6`;
do
    python make_index.py 2007 $mo
    zcat output/index_s_2007* | sort | gzip -9 > index_s_yr2007.tsv.gz
    zcat output/index_m_2007*.tsv.gz | sort -t $'\t' -k 3,3 -k 2,2 | gzip -9 > index_m_yr2007.tsv.gz
done

exit 0

# for all other years, 12 months of data, set you data ranges
for yr in `seq 2006 2006`;
do
    for mo in `seq 1 12`;
    do
        python make_index.py $yr $mo
    done
    zcat output/index_s_$yr* | sort | gzip -9 > index_s_yr$yr.tsv.gz
    zcat output/index_m_$yr*.tsv.gz | sort -t $'\t' -k 3,3 -k 2,2 | gzip -9 > index_m_yr$yr.tsv.gz
done

