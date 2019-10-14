#!/bin/bash

# remove predictions: change, not - and not + from a prediction file
# ----------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive functional networks: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

# Usage:
#   bash remove_change.sh prediction_file > new_prediction_file
# where prediction_file is a prediction file issued from IGGY
# Output:
#   prediction file without change, not - and not + predictions
#
# Example:
#   sh remove_complexes.sh prediction.tsv > prediction_change.tsv
# 

PRED_FILE="$1"



# Check presence of files
if [ ! -f "$PRED_FILE" ]
then
  echo "File $PRED_FILE does not exist"
  exit 1
fi

sed '/CHANGE/d' "$PRED_FILE" > ./supmat/3-iggy/data/2345-result-nochange.tsv
