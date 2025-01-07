### Get Start

```
conda env list
conda env remove --name pypsa-eur
conda env create -f envs/environment.yaml
conda activate pypsa-eur


snakemake -call all --configfile work/base/baseEUDE2045.yaml --cores all
snakemake prepare_sector_networks --configfile work/base/baseEUDE2045.yaml --cores all

```


### other information

DE 39