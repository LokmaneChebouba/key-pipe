#!/bin/bash

# Run computation and tests for the statistical validation 
# --------------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# Hepatocellular carcinoma computational models identify key protein-complexes associated to tumor progression
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

# WARNING:
#   The computation of all runs may take a very long time!
#   With 1 min per run on an Intel Core i7-6600U CPU, 2.60GHz×4 laptop, it takes 30 h.
#   It is recommended to launch this computation on a cluster (or on your week-end).
#   You can also change the values below.

# Parameters of the statistical random sampling:
START_SAMPLING=$3    # Sampling start percentage (f.i. 10)
STOP_SAMPLING=$4     # Sampling stop percentage (f.i. 95)
STEP_SAMPLING=$5      # Sampling percentage step (f.i. 5)
NUMBER_RUNS=$6      # Number of runs for each sampling (f.i. 100)

# If needed, specify your Iggy command here:
IGGY="${HOME}/.local/bin/iggy.py"



# Compute all runs for all samplings
#OUTDIR="prp-${START_SAMPLING}-${STOP_SAMPLING}-${STEP_SAMPLING}-${NUMBER_RUNS}/"
OUTDIR="./supmat/4-validation/output"

#construct all the positive nodes on a file, and all negative nodes in another
sh ./supmat/4-validation/scripts/construct_trueup_truedown.sh ./supmat/2-pathrider/data/out-filtered.sif ./supmat/2-pathrider/data/updown-noinputs_gen2.obs
#time python ./supmat/4-validation/scripts/pickrandom-percentage.py --scripts-path ./supmat/3-iggy/scripts/ --iggy-command "$IGGY" ./supmat/2-graph-extraction/data/graph.sif ./supmat/1-diff-analysis/data/GSEA_EMThigh_vs_EMTlow_diffexp.csv ./supmat/4-validation/data/name-true-up_gen.csv ./supmat/4-validation/data/name-true-down_gen.csv $START_SAMPLING $STOP_SAMPLING $STEP_SAMPLING $NUMBER_RUNS "$OUTDIR"
time python3 ./supmat/4-validation/scripts/pickrandom-percentage.py --scripts-path ./supmat/3-iggy/scripts/ --iggy-command "$IGGY" ./supmat/2-pathrider/data/out-filtered.sif $2 ./supmat/4-validation/data/name-true-up_gen.csv ./supmat/4-validation/data/name-true-down_gen.csv $START_SAMPLING $STOP_SAMPLING $STEP_SAMPLING $NUMBER_RUNS "$OUTDIR"

#mkdir "$OUTDIR/plots"

# Compute stability stats
#python ./supmat/4-validation/scripts/stats-robustness.py "$OUTDIR" "robustness-brief-nochange.tsv" --complete-pred ./supmat/3-iggy/data/2345-result-nochange.tsv --brief-weak --sum-all --verbose -ncp -100 -d plots

# Compute robustness stats
#python ./supmat/4-validation/scripts/stats-matrixscore.py "$OUTDIR" m2.tsv --detail-scores --complete-pred ./supmat/3-iggy/data/2345-result-nochange.tsv --export-plot --dest-plot plots --verbose

