#!/bin/bash

# Run information extraction from the graph and ICGC file
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

#create data folders
rm -r ./supmat/2-pathrider/data
mkdir ./supmat/2-pathrider/data
rm -r ./supmat/3-iggy/data
mkdir ./supmat/3-iggy/data
rm -r ./supmat/4-validation/data
mkdir ./supmat/4-validation/data

echo "Reading $1.."
#construction of the observation from the icgc file
sh ./supmat/1-graph-extraction/scripts/obs_construction.sh $1
echo "Writing gene names"
echo "writing observations"

