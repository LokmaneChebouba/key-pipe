#!/bin/bash

# Compute predictions with Iggy
# -----------------------------
# This file is part of the Supplementary Material of the submission entitled:
# Hepatocellular carcinoma computational models identify key protein-complexes associated to tumor progression
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret
# Install Iggy with:
#   $ pip install --user iggy==1.4.1
# Then specify the path to iggy.py in the following line:
IGGY="${HOME}/.local/bin/iggy.py"
echo "Reading graph filtered.."
echo "Reading observations.."
echo "Reading ICGC file.."
# Construct final observations file including inputs (nodes without predecessors)
#bash ./supmat/3-iggy/scripts/construct-inputs.sh --gen ./supmat/2-graph-extraction/data/graph.sif ./supmat/1-diff-analysis/data/updown-noinputs_gen.obs > "2345.obs"
bash ./supmat/3-iggy/scripts/construct-inputs.sh --gen ./supmat/2-pathrider/data/out-filtered.sif ./supmat/2-pathrider/data/updown-noinputs_gen.obs > ./supmat/3-iggy/data/2345.obs

# Call the full workflow (Iggy + post-processing of results)
#sh ./supmat/3-iggy/scripts/workflow-iggy.sh --gen --iggy-command "$IGGY" ./supmat/3-iggy/data/2345.obs ./supmat/2-graph-extraction/data/graph.sif ./supmat/1-diff-analysis/data/GSEA_EMThigh_vs_EMTlow_diffexp.csv 0 0 "2345.out" > "2345-result.tsv"
echo "Running Iggy and comparaison with ICGC.."
sh ./supmat/3-iggy/scripts/workflow-iggy.sh --gen --iggy-command "$IGGY" ./supmat/3-iggy/data/2345.obs ./supmat/2-pathrider/data/out-filtered.sif $1 0 0 "./supmat/3-iggy/data/2345.out" > ./supmat/3-iggy/data/2345-result.tsv
echo "Writing predictions.."
#remove change, not + and not -
sh ./supmat/3-iggy/scripts/remove_change.sh ./supmat/3-iggy/data/2345-result.tsv > ./supmat/3-iggy/data/2345-result-nochange.tsv

# Statistics on the results
#bash ./supmat/3-iggy/scripts/stats-result.sh --en --skip0 "2345-result.tsv" ./supmat/2-graph-extraction/data/graph.sif
bash ./supmat/3-iggy/scripts/stats-result.sh --en --skip0 ./supmat/3-iggy/data/2345-result.tsv ./supmat/3-iggy/data/2345.obs ./supmat/2-pathrider/data/out-filtered.sif

