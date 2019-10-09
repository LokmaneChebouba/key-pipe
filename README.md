# key-pipeline
A computational model to identify key protein-complexes associated to tumor progression

## 1 Introduction
We introduce the `key-pipeline`, a python package implementing a workflow for identifying key protein-complexes associated to tumor progression. From an initial network and a set of experimental data on gene expression, our software allows researchers to
(i) find the upstream/downstream paths starting from a couple of root nodes in a network using [pathrider](https://github.com/arnaudporet/pathrider), a tool developed in our team to this purpose,
(ii) check the consistency of the experimental data set, provide repairs for inconsistencies and make preidctions using the existing [iggy](http://bioasp.github.io/iggy/) tool,
(iii) validate the predictions made by iggy by computing the number of predictions matching the related experimental fold-change from the experimental data,
(iv) perform precision and stability tests by comparing prediction on subsets of observations with predictions using all observations, and finally
(v) plot both precision scores for each sampling, and the evolution of the prediction compared to the entire set of observations.

## 2 Prerequisites
`key-pipeline` is a Python application that uses several libraries and tools.

##### With Python already installed
If you already have Python installed, you can install and configure automatically conda by running either `config_Linux.py` or `config_MacOS.py` in the `key-pipeline` folder using:

```
$ python config_<your_OS>.py
```

##### Without Python already installed
If Python is not installed on your machine yet, the easiest way is to download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for Python 3.7.
Once Miniconda is installed, use the `environment.yml` file in the `key-pipeline` folder to configure the environment by runing:

```
$ conda env create -f environment.yml
```

The `environment.yml` file contains all depencies required for the successful execution of the pipeline.

##### Activation/Deactivation of pip-env environment
After following either of the two cases above, an environment named `pip-env` with all required dependencies (Python, iggy, plotly, etc.) should be created.
To activate this environment, use:

```
$ conda activate pip-env
```

To deactivate an active environment, use:

```
$ conda deactivate
```

##### Example of `requirements.yml` file
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

## 3 Usage
Our tool provides a script that can be used in a command line interface (CLI), and customized by giving arguments.
Default arguments are provided in the `arguments.txt` file.
By default, all the steps of the methods will be run; if you want to run just one or more steps, you can enter the number of steps you want by using `--steps` and the number of desired step separated by ”,”.
The argument `--help` provides the help message describing required inputs and available options.

This script calls all the steps in the workflow described in the article.
Each step will output one or more files.
In general, the output of one step corresponds to the input of the following ones.
This enables a straightforward application of the workflow for users without programming expertise.

If not already done, first activate the pipeline environment:

```
$ conda activate pip-env
```

Then, from the `key-pipeline` folder, run:

```
$ python pipe.py @arguments.txt
```

##### Example of arguments file

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
$ python pipe.py --help
```

> ```
> usage: Usage: python pipe.py @arguments_file [--steps]
> 
> Pipeline HCC: require a file preceded by '@' and must contain all the required
> arguments cited below:
> 
> optional arguments:
>   -h, --help            show this help message and exit
> 
> optional arguments:
>   --dir DIR             follows the up stream ('up') or the down stream
>                         ('down'). Default to 'up'
>   --steps STEPS         specify the number of the steps to run: [1] Graph
>                         extraction [2] Pathrider [3] Iggy [4] Cross-Validation
>                         [5] Plots. (If many, separate by ','). Default run all
>                         steps
>   --start_sampling START_SAMPLING
>                         The start sampling percentage. Default= 10
>   --stop_sampling STOP_SAMPLING
>                         The stop sampling percentage. Default= 100
>   --step_sampling STEP_SAMPLING
>                         The step of sampling. Default= 5
>   --numbers_run NUMBERS_RUN
>                         The number of runs on each step. Default= 100
> 
> required arguments:
>   --sif SIF             influence graph in SIF format
>   --icgc ICGC           ICGC file
>   --b B                 a list of blacklisted genes (weakly expressed)
> ```

##### Example 1:
```
python pipe.py @arguments.txt
```
This command will run all the steps of our method (1..5).

##### Example 2:
```
python pipe.py @arguments.txt --steps 3
```
This command will run only step 3 of our method.

##### Example 3:
```
python pipe.py @arguments.txt --steps 4,5
```
This command will run steps 4 and 5 of our method.

## Warning
Every time you launch the tool, it will overwrite the data produced during previous launches. If you need it, think of saving it under another name.

##### Assumptions 
We assume that the network provided in the arguments file is in [SIF format](https://cytoscape.org/manual/Cytoscape2_5Manual.html#SIF%20Format).

##### Case study
An example for hepatocellular carcinoma (HCC) is provided under the folder `example`, providing:

- a KEGG graph extraction (in SIF format),
- the differential expression data obtained from ICGC data (in CSV format),
- a list of blacklisted species.

This is intended for immediate use and these files are already specified in the `arguments.txt` file.
Moreover, the following default values are given for the stability study:

- start sampling percentage = 10,
- stop sampling percentage = 15,
- step sampling = 5,
- number of runs = 2.

These values are not recommended for a complete analysis but as this step is very long, only small values are provided in order to avoid letting the script run for too long.

## 4 Detailed Steps
Each step of the tool requires some inputs and produces outputs.
Each step is represented by a folder in `key-pipeline/supmat` under which there alreay exists a `scripts` folder that contains all scripts needed.
When the pipeline is launched, `data` folders are added which are inteded to contain the input/output data.

#### 4.1. Threshold extraction

##### input
* The global primary network file
* Experimental data (e.g. ICGC data)

##### output
* Components names
* Observations file

#### 4.2. Extracting regulatory signaling pathways (Pathrider)

##### input
* The global primary network file
* Components names
* Blacklist

##### output
* The final network filtered with the observed nodes we have

#### 4.3. Prediction (Iggy)

##### input
* The filtered network
* Observations file
* Experimental data

##### output
* Predictions

#### 4.4. Validation, Robustness and precision

##### input
* The filtered network
* Observations file
* Experimental data
* Sampling parameters

##### output
* Sets of predictions

#### 4.5. Plot

##### input
* Predictions from step 3
* Sets of predictions from step 4

##### output
* Prediction stability plot
* Robustness plot

