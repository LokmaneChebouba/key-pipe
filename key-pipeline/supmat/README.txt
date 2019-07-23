
Supplementary material of the submission entitled:
====================================================================================================================
=== Hepatocellular carcinoma computational models identify key protein-complexes associated to tumor progression ===
====================================================================================================================
and authored by: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret
==============================================================================================================

Please refer to the decriptions below and to the files themselves for purpose and usage.



===============
=== License ===
===============

Except for content originating from other sources (ICGC, KEGG, etc.) and already subject to other licences, all content in this archive (scripts, data, figures, etc.) is published under the terms of the Creative Commons Attribution 4.0 International (CC BY 4.0) license, which is available at: https://creativecommons.org/licenses/by/4.0/
This licence grants you the right to copy, modify and share your modifications, under the condition that you give credit for all authors of this work.



====================
=== Requirements ===
====================

A Bash or compatible Unix-like shell is required for all shell scripts (native on GNU/Linux of Mac OS systems).
Python 3.6 is required for all Python scripts.
R (statistical computing environment) is required to run the differential expression analysis (part 1).
Iggy version 1.4.1 is required to compute predictions (parts 3 & 4).
go is required to run pathrider tool

One simple way to install these requirements is by downloading and installing Anaconda or Miniconda:
  https://docs.conda.io/en/latest/miniconda.html

After that, you can run the following commands to install all requirements:
  conda install pip r r-gplots r-RColorBrewer
  pip install --user iggy==1.4.1



==================
=== Main files ===
==================

Cytoscape session of the whole graph:
=================--------------------
  - 2-graph-extraction/data/graph.cys

Interactive volcano plots with gene names on mouse hover:
------------=============--------------------------------
  - 5-plots/volcano1-all-genes.html
  - 5-plots/volcano2-predictions.html

Scripts to run parts of the analysis:
=======------------------------------
  - 1-diff-analysis/scripts/download-and-run.sh
  - 3-iggy/scripts/run-iggy.sh
  - 4-validation/scripts/run-validation.sh



============================
=== Folders and contents ===
============================

  - 1-diff-analysis: Data and scripts for the differential analysis and clustering on ICGC gene expression data
    - data
      - GSEA_EMThigh_vs_EMTlow_diffexp.csv: result of the differential expression (all genes except undetectable)
      - LIHC_primary_weakly_expressed_genes.txt: list of undetectable genes excluded from analysis
      - diffexp_filtered.csv: only genes differentially over- and under-expressed: log(fold-change) > 2 or < −0.5 and P-val < 10^−5
      - updown-noinputs_gen.obs: same list, formatted for Iggy
    - scripts
      - download-and-run.sh: Fetch and filter data, and perform differential expression analysis and clustering
      - dataset_filtering.sh: Dataset filtering
      - diffexp_and_clustering.R: Clustering and differential expression analysis + plots

  - 2-graph-extraction: Graph extracted from Kegg and filtered using Stream
    - data
      - graph.sif: SIF version of the graph, formatted for use with Iggy
      - graph.cys: Cytoscape session of the graph with mapping of the results (see Cytoscape styles)

  - 3-iggy: Data and scripts for the predictions computation with Iggy
    - data
      - 2345.obs: Observations file formatted for Iggy
      - 2345-result.tsv: Result of the computation of predictions by Iggy
      - 2345-result-nochange.tsv: Same file, excluding the two “CHANGE” weak predictions
    - scripts
      - run-iggy.sh: Execute the full execution pipeline for Iggy on the provided files
      - workflow-iggy.sh: Call Iggy and post-process the results
      - stats-result.sh: Extract statistics on the post-processed results of Iggy
      - (others): Various scripts used in the workflow

  - 4-validation
    - data
      - name-true-up_gen.csv, name-true-down_gen.csv: List of over- and under-expressed genes actually in the graph
    - scripts
      - run-validation.sh: Compute the whole statistical validation and produce interactive plots
      - pickrandom-percentage.py: Compute the samplings and runs of Iggy with partial observations
      - stats-matrixscore.py: Compute recovery rate study on the results, outputs a plot
      - stats-robustness.py: Compute stability study on the results, outputs a plot
      - (others): Libraries and configuration files for the statistical validation

  - 5-plots
    - volcano1-all-genes.html: Interactive volcano plot of the fold-change and distribution of those in the graph
    - volcano2-predictions.html: Same interactive volcano plot with prediction results mapped on the nodes
    - boxplot-recovery-rate.html: Interactive plot of the recovery rate study
    - plot-stability.html: Interactive plot of the stability study



=======================
=== Other resources ===
=======================

The Iggy tool is available at:
  http://bioasp.github.io/iggy/

The Stream tool (without the blacklist feature used in this work) is available at:
  https://github.com/arnaudporet/stream

Experimental gene expression data (LIHC-US project, release 21) can be downloaded from ICGC at:
  https://dcc.icgc.org/releases/release_21/Projects/LIHC-US

