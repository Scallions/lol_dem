key=Haworth1
if [ -n "$1" ]
then
	key=$1
fi
# echo "key: $key"
# python scripts/rename_sparse_orbit.py -k $key

# python scripts/rename_worst_orbit.py -k $key
# python scripts/cross_point.py -k $key
# python scripts/remove_crossover_point.py -k $key

python scripts/rename_time_range.py -k $key

# 去粗差
python scripts/remove_outlier.py -k $key
python scripts/rename_discrete_orbit.py -k $key -t O
python scripts/rename_sparse_orbit.py -k $key -t O

## 平差
python scripts/cross_point.py -k $key
python scripts/rename_worst_orbit.py -k $key 
python scripts/cross_point.py -k $key
python scripts/cross_over_adj.py -k $key
python scripts/cross_point_post.py -k $key
python scripts/cross_point_stat.py -k $key

## 生成 平差后 csv
python scripts/gen_csv.py -k $key -t C