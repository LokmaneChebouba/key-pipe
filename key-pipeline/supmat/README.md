# Scripts and output data of the pipeline

## Purpose
These folders contain a sub-folder `scripts` containing all scripts intended for the general pipeline.
Once the pipeline is launched, another sub-folder `data` is also created in order to store the outputs of each step and inputs for the following steps.

Use the `pipe.py` script in the parent folder to use these scripts.
Example data is provided in the example folder at the root of the project.

## Folders description
- `1-graph-extraction` : build observations from differential expression data
- `2-pathrider` : extract graph from observation nodes using Pathrider
- `3-iggy` : compute predictions from graph and observations with Iggy
- `4-validation` : compute validation on random subsets of observations
- `5-plots` : build plots summing up the validation step

## Build a Cytoscape session
Once you have run the pipeline at least up to step 3 (Iggy), you are able to build a Cytoscape session from the files produced.
To do so, as the network file, provide `2-pathrider/data/out-filtered.sif`
and as a table file, provide `3-iggy/data/2345-result.tsv`.
As a result, the edges will be labeled with their types (activation or inhibition) and the nodes will be labeled with the type of observation (`obs:+` or `obs:-`) or prediction (`pred:+`, `pred:-`, etc.), allowing you to apply cutsom styles.

