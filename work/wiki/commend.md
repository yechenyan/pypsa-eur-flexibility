### Get Start

```
conda env list
conda env remove --name pypsa-eur
conda env create -f envs/environment.yaml
conda activate pypsa-eur

snakemake -call all --configfile work/base/baseSimple2045.yaml --cores all
snakemake prepare_sector_networks --configfile work/test/testGeothermal2045.yaml --cores all





```
