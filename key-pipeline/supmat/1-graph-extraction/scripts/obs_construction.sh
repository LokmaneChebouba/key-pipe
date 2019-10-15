#!/bin/bash

# 1- construct the observation file from diffexp_interest genes issued from ICGC data
# 2- construct gene names (genes of interest)
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive functional networks: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

# Load experimental (ICGC) data and extract the relevant observations
#
# Usage:
#   bash obs_construction.sh icgc_data.csv
# where icgc_data is the experimental data file (for instance ICGC data) in TSV format containing
# at least 3 columns: gene names, fold-change and p-value (the other columns are ignored).
#
# Output: two files are created
#   - genes_name.txt: name column file (X_gen)
#   - updown-noinputs_gen.obs: observation file without suffixes (X = +/-)
#   - updown-noinputs_gen2.obs: observation file (X_gen = +/-)
#
# Example:
#   sh obs_construction.sh ../../../../example/GSEA_EMThigh_vs_EMTlow_diffexp.csv
# 

if [ -z "$1" ]
then
  echo "Usage: bash obs_construction.sh icgc_data.csv"
  echo "where icgc_data.csv is the experimental data file in TSV format"
  echo "containing gene names, fold-change and p-values"
  exit
fi


awk -F"\t" 'FNR > 1 {if ($2 > 2  && -log($3)/log(10)>5) print $1 "_gen = +"; else if ($2 < -0.5 && -log($3)/log(10)>5) print $1 "_gen = -";}' "$1" > ./supmat/2-pathrider/data/updown-noinputs_gen2.obs
awk -F"\t" 'FNR > 1 {if ($2 > 2  && -log($3)/log(10)>5) print $1 " = +"; else if ($2 < -0.5 && -log($3)/log(10)>5) print $1 " = -";}' "$1" > ./supmat/2-pathrider/data/updown-noinputs_gen.obs

#construct column_name.txt
awk -F" " '{print $1}' ./supmat/2-pathrider/data/updown-noinputs_gen2.obs  > ./supmat/2-pathrider/data/genes_name.txt
