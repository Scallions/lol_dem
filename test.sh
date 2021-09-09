key=small1
if [ -n "$1" ]
then
	key=$1
fi
# echo "key: $key"
# python scripts/remove_outlier.py -k $key
# python scripts/rename_sparse_orbit.py -k $key
python scripts/rename_discrete_orbit.py -k $key
python scripts/cross_point.py -k $key
# python scripts/rename_worst_orbit.py -k $key
python scripts/cross_over_adj.py -k $key
# python scripts/cross_point.py -k $key
# python scripts/remove_crossover_point.py -k $key
# python scripts/gen_csv.py -k $key
python scripts/cross_point_post.py -k $key
