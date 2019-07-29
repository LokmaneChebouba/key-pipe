#!/bin/bash

# Run information extraction from the graph and ICGC file
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret


#run pathrider 

echo "Reading $3.."
#create black list with genes and proteins
sh ./supmat/2-pathrider/scripts/excluded_gen_prot.sh $3

echo "Reading $1.."
echo "Reading gene names.."
echo "Running Pathrider..."
#./supmat/2-pathrider/scripts/pathrider stream $1 $2 $3 #-blacklist ./supmat/0-diff-analysis/data/LIHC_primary_weakly_expressed_genes.txt
go run ./supmat/2-pathrider/scripts/pathrider/pathrider.go stream -blacklist ./supmat/2-pathrider/data/excluded_gen_prot.txt -out ./supmat/2-pathrider/data/out_pathrider.sif $1 ./supmat/2-pathrider/data/genes_name.txt $2 > ./supmat/2-pathrider/pathrider_out.out
#filter the graph from a black list
#sh ./supmat/2-pathrider/scripts/remove_complexes.sh ./supmat/2-pathrider/data/out_pathrider.sif
grep -wvi -f $3 ./supmat/2-pathrider/data/out_pathrider.sif > ./supmat/2-pathrider/data/out-filtered.sif
echo "Writing graph filtered"

