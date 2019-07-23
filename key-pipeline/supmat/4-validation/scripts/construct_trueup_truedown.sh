#!/bin/bash

# 1- construct the observation file from diffexp_interest genes issued from ICGC data
# 2- construct gene names (genes of interest)
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

# Usage:
#   bash construct_trueup_truedown.sh sif-file obs-file > name-true-up_gen.csv name-true-down_gen.csv
# where <SIF file> is a SIF file you want the genes extracted from
# and <obs file> is a preliminary Iggy observation file containing only “ = +” and “ = -” observations
#
# Output:
#   1- name-true-up_gen
#   2- name-down-up_gen
#
# Example:
#   sh obs_construction.sh graph.sif 2345.obs
# 

SIF_FILE="$1"
OBS_FILE="$2"

# Check arguments
if [ -z "$OBS_FILE" ]
then
  echo "Usage:"
  echo "  bash construct_trueup_truedown.sh sif-file obs-file > name-true-up_gen.csv name-true-down_gen.csv"
  echo "Create two files, genes observed as +, and genes observed as -"
  exit 1
fi

# Check presence of files
if [ ! -f "$SIF_FILE" ]
then
  echo "File $SIF_FILE does not exist"
  exit 1
fi

if [ ! -f "$OBS_FILE" ]
then
  echo "File $OBS_FILE does not exist"
  exit 1
fi

#cut -f 1 "$SIF_FILE" > ../data/list_sif
#awk 'NR==FNR{A[$1];next}$2 in A' "$OBS_FILE" "$SIF_FILE" > ../data/out
#awk -F'\t' '$1!=$2 {print $1,"==",$1}' "$OBS_FILE" "$SIF_FILE" > ../data/out

#create a temporary directory
mkdir ./supmat/4-validation/data/tmp

#extract all node + (resp -) nodes in a separated file
awk -F" " 'FNR > 1 !NF || !seen[$3]++ {if ($3=="+") print $1}' "$OBS_FILE" > ./supmat/4-validation/data/tmp/all-true-up_gen.csv
awk -F" " 'FNR > 1 !NF || !seen[$3]++ {if ($3=="-") print $1}' "$OBS_FILE" > ./supmat/4-validation/data/tmp/all-true-down_gen.csv

#put all the nodes in the sif file on one column
awk -F" " '!NF || !seen[$1]++ {print $1} !NF || !seen[$3]++ {print $3}' "$SIF_FILE" > ./supmat/4-validation/data/tmp/new_sif.csv

#awk -F"\t" 'FNR > 1 {print $1 }' "$OBS_FILE" > ../data/obs1.csv
#awk -F"\t" 'FNR > 1 {print $1 }' "$SIF_FILE" > ../data/sif1.csv

#sort files
sort +0 ./supmat/4-validation/data/tmp/all-true-up_gen.csv > ./supmat/4-validation/data/tmp/obs1.csv
sort +0 ./supmat/4-validation/data/tmp/all-true-down_gen.csv > ./supmat/4-validation/data/tmp/obs2.csv
sort +0 ./supmat/4-validation/data/tmp/new_sif.csv > ./supmat/4-validation/data/tmp/new_sif2.csv

#intersection between file 1 and file 2
comm -12 ./supmat/4-validation/data/tmp/obs1.csv ./supmat/4-validation/data/tmp/new_sif2.csv > ./supmat/4-validation/data/name-true-up_gen.csv
comm -12 ./supmat/4-validation/data/tmp/obs2.csv ./supmat/4-validation/data/tmp/new_sif2.csv > ./supmat/4-validation/data/name-true-down_gen.csv
#remove temporary directory
rm -r ./supmat/4-validation/data/tmp
