#!/bin/bash

# Run information extraction from the graph and ICGC file
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

#create data folders
if [ ! -d ./supmat/2-pathrider/data ]; then
  mkdir -p ./supmat/2-pathrider/data;
fi
if [ ! -d ./supmat/3-iggy/data ]; then
  mkdir -p ./supmat/3-iggy/data;
fi
if [ ! -d ./supmat/4-validation/data ]; then
  mkdir -p ./supmat/4-validation/data;
fi

echo "Reading $1.."
#construction of the observation from the icgc file
sh ./supmat/1-graph-extraction/scripts/obs_construction.sh $1
echo "Writing gene names"
echo "writing observations"

