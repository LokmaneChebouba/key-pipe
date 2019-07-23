#!/bin/bash

# remove complexes from the sif file
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

# Usage:
#   bash remove_complexes.sh sif-file > new_sif
# where <SIF file> is a SIF file on which you want to remove complexes
# Output:
#   sif file without complexes
#
# Example:
#   sh remove_complexes.sh sif.sif > new_sif.sif
# 

SIF_FILE="$1"



# Check presence of files
if [ ! -f "$SIF_FILE" ]
then
  echo "File $SIF_FILE does not exist"
  exit 1
fi

#sed '/::/d' "$SIF_FILE" > ./supmat/2-pathrider/data/hsa_without_complexes_graph.sif
grep -wvi -f ./supmat/0-diff-analysis/data/name-weakly_expressed.txt "$SIF_FILE" > ./supmat/2-pathrider/data/hsa-2345-out-filtered.sif
