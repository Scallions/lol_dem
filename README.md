some code about moon dem ( T T )

## 交叉点平差

计划采用偏差倾斜式轨道误差，由于是月球测高，地面误差不过多考虑

altimeter data:
- http://pds-geosciences.wustl.edu/

计划的技术栈
- GSL： 科学计算库
- boost： 文件处理
- xmake： 项目编译
- python： 数据爬取
- pygmt： 数据可视化
- 克里金插值生成格网数据

some docs:
- https://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/catalog/rdr_ds.cat


some key data description
- 10-12m apart along track
- 5m diameter observation area
- 20m FOV
- profiles 10-12m apart
- 50m two sample

normal without header and line index
file format:
- *.DAT: binary data file
- *.[A|D]R: txt raw data file 
- *.[A|D]F: fuse data file
- *.[A|D]O: remove outlier
- *.[A|D]OF: fuse remove outlier
- *.[A|D]C: after crossover adj

## config 设置
在根目录创建`config.ini`

```
[DEFAULT]
dir = ./data/202,222,-86,-84
region = 202,222,-86,-84
adj = no
fuse = no
iter = 2

[custom]
dir = ./datas/shoemaker,18,74,-89,-85
region = 18,74,-89,-85
```
根据需要在 `custom` 里面覆盖默认设置

## outlier
1. win_size 20, iqr
2. win_size 10, iqr
3. win_size 10, remove trend with moving mean + iqr

## 使用步骤 
- read_data
- remove outlier
- rename track
- crossover
- remove cps
- adj
	- post crossover
	- remove cps
	- analysis
- dem

## TODO
- sparse matrix
- multiple thread
- simulation experiment