#!/bin/bash

# construct a list of genes and proteins from a list of nodes
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

# Usage:
#   bash black_list_gen_prot.sh txt > new_txt
# where <txt file> is a text file that contain one node per line
# Output:
#   sif file without complexes
#
# Example:
#   sh black_list_gen_prot.sh black_list.txt
# 

BLACK_FILE="$1"



# Check presence of files
if [ ! -f "$BLACK_FILE" ]
then
  echo "File $BLACK_FILE does not exist"
  exit 1
fi

awk '{print $1 "_gen"; print $1 "_prot"}' "$1" > ./supmat/2-pathrider/data/black_list_gen_prot.txt
