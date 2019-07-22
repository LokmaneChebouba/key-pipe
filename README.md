### Readme to be completed..
# key-pipeline
A computational model to identify key protein-complexes associated to tumor progression
### 1 Introduction
We introduce the ```key-pipeline```, a python package implementing a workflow for identifying key protein-complexes associated to tumor progression. Our software allows researchers to (i) find the upstream/downstream paths starting from a
couple of root nodes in a network using [pathrider](https://github.com/arnaudporet/pathrider) , a tool developed in our team
to this purpose; (ii) then check the consistency of our data sets and provides explanations for inconsistencies using iggy tool; (iii) validate the predictions made by iggy by computing the number of predictions matching the related experimental fold-change from ICGC data; (iv) design a stability test by comparing prediction on subsets of observations with predictions using all observations; and finally (v) plot both precision scores for each sampling, and the evolution of the prediction compared to the entire set of observations.
### 2 Prerequisites
key-pipeline is a python application that uses many libraries and tools. The easiest way to obtain all depencies packages is using Anaconda. First install either Anaconda or Miniconda, then download environment.yml file to configure the environment and then run:

```
$ conda env create -f environment.yml
```
The ```environment.yml``` file contain all depencies required for the successful execution of the program.\

###### Example of requirements file
```
name: pip-env
channels:
  - default
dependencies:
  - plotly==3.10.0
  - python==3.7.3
  - go
  - pip
  - pip:
    - iggy==1.4.1
```
This will create ```key-pip``` environment with all dependencies.
In this case, the packages plotly, python.. will be installed.
To activate this environment, use:
```
$ conda activate pip-env
```
To deactivate an active environment, use:
```
$ conda deactivate
```

### 3 Usage
Our tool provides a command line interface (CLI), it can be run by entering the arguments file (see below). By default, all the steps of the methods will be run, if you want to run just one or more steps, you can enter the number of steps you want by using ```--steps``` and the number of desired step separated by ”,”. The ```--help``` provides the help message describing required inputs and available options. It implements all the steps in the workflow described before. Each step will output one or more files. In general, the output of one step corresponds to the input of another one. This enables a straightforward application of the workflow for users without programming expertise. \
After the activation of the environment, from the main folder run:
```
$ python pipe.py @arguments.txt
```
Where ```arguments.txt``` contains all the arguments needed for the execution of the pipeline.\

###### Example of arguments file

Here is an example of an arguments file:
```
--sif=/home/graph.sif
--icgc=/home/ICGC_data.csv
--start_sampling=10
--stop_sampling=15
--step_sampling=5
--numbers_run=2
```
For more options you can ask for help:
```
$ python pipe.py @arguments.txt --help
```
```
usage: Usage : python pipe.py@arguments_file [--steps]
key-pipeline: require a file preceded by ’@’ and must contain all the required arguments cited below :
optional arguments :
-h , --help   show this help message and exit
optional arguments :
--dir DIR     follows the up stream ( ”up” ) or the down stream ( ”down” )
--steps STEPS     specify the number of the steps to run :
[ 1 ] Graph extraction
[ 2 ] Pathfinder
[ 3 ] Iggy
[ 4 ] Cross-Validation
[ 5 ] Plots
( I f many ,separate by ’,’). Default run all steps
--start_sampling START_SAMPLING    The start sampling percentage. Default=10
--stop_sampling STOP_SAMPLING     The stop sampling percentage. Default=100
--step_sampling STEP_SAMPLING     The step of sampling. Default=5
--numbers_run NUMBERS_RUN     The number of runs on each step. Default=100
requiredarguments:
--sif SIF     influence graph in SIF format
--icgc ICGC     ICGC file
```
###### Assumptions 
We assume that the network provided in the arguments file must be in the SIF file format
###### Case studie
An example for hepatocellular carcinoma (hcc) is provided under the folder ```example```, the KEGG graph extraction (in SIF format), the differential expression data obtained from ICGC data (in CSV format), the blacklisted species, and the validation parameters start sampling, stopsampling, step sampling, numbers run).

### 4 Steps
Each step of the tool need some inputs, and produce outputs:
