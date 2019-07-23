#!/bin/bash

# 1- construct the observation file from diffexp_interest genes issued from ICGC data
# 2- construct gene names (genes of interest)
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

# Usage:
#   bash obs_construction.sh icgc_filtered.csv > results-file
# where icgc_filtered is the ICGC file with just genes of interest (filtered)
# and results-file is a file containing the output;
#
# Output:
#   1- observation file (X_gen = +/-)
#   2- name column file (X_gen)
#
# Example:
#   sh obs_construction.sh icgc_filtered.csv 2345.obs
# 

if [ -z "$1" ]
then
  echo "Usage: sh obs_construction.sh icgc_filtered.csv > results-file" #donner GSEA_... 
  echo "icgc_filtered is the ICGC file with just genes of interest (filtered)"
  echo "and results-file is a file containing the output"
  exit
fi


awk -F"\t" 'FNR > 1 {if ($2 > 2  && -log($3)/log(10)>5) print $1 "_gen = +"; else if ($2 < -0.5 && -log($3)/log(10)>5) print $1 "_gen = -";}' "$1" > ./supmat/2-pathrider/data/updown-noinputs_gen2.obs #trouver la bonne formule -log2$3
awk -F"\t" 'FNR > 1 {if ($2 > 2  && -log($3)/log(10)>5) print $1 " = +"; else if ($2 < -0.5 && -log($3)/log(10)>5) print $1 " = -";}' "$1" > ./supmat/2-pathrider/data/updown-noinputs_gen.obs

#construct column_name.txt
awk -F" " '{print $1}' ./supmat/2-pathrider/data/updown-noinputs_gen2.obs  > ./supmat/2-pathrider/data/column_name.txt
