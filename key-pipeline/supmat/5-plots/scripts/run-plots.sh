#!/bin/python3
#coding=utf-8

# Draw plots from the statistical validation
# ----------------------------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# Hepatocellular carcinoma computational models identify key protein-complexes associated to tumor progression
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

OUTDIR="./supmat/4-validation/output"
#mkdir "./supmat/5-plots/plots"
mkdir "./supmat/5-plots/plots"

# Compute stability stats
python ./supmat/4-validation/scripts/stats-robustness.py "$OUTDIR" "robustness-brief-nochange.tsv" --complete-pred ./supmat/3-iggy/data/2345-result-nochange.tsv --brief-weak --sum-all --verbose -ncp -100 -d ../../5-plots/plots

# Compute robustness stats
python ./supmat/4-validation/scripts/stats-matrixscore.py "$OUTDIR" m2.tsv --detail-scores --complete-pred ./supmat/3-iggy/data/2345-result-nochange.tsv --export-plot --dest-plot ../../5-plots/plots --verbose

