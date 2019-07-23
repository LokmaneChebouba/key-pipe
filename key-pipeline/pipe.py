import sys
import argparse
import os
import optparse
import fileinput
import string
from argparse import ArgumentParser
#from pyasp.asp import *
#from __iggy__ import query, utils, parsers

# -------------------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret


def diffanalysis():
  print('----------- [1] Pre-treatment -----------')
  os.system('sh ./supmat/1-graph-extraction/scripts/run-extract.sh %s' % (ns.icgc))
def pathrider():
  print('----------- [2] Run pathrider -----------')
  param = 'sh ./supmat/2-pathrider/scripts/run-pathrider.sh %s %s %s' % (ns.sif, ns.dir, ns.b)
  #param1 = 'go run ./supmat/2-pathrider/scripts/pathrider/pathrider.go %s ./supmat/2-pathrider/data/column_name.csv %s' % (ns.sif, ns.dir)
  #go run pathrider.go sif file nodes_name.txt up (se positionner au repertoire de pathrider)
  #os.system(param1)
  os.system(param)
  
  #traiter le résultat de pathrider (1 et -1)
  #file = '/home/computer/.local/bin/supmat/2-graph-extraction/data/graphesteam.sif'
  #for line in fileinput.FileInput(file, inplace=1):
    #line=line.replace("activation_PPrel,phosphorylation_PPrel","1")
    #line=line.replace("activation_PPrel","1")
    #line=line.replace("indirect effect_PPrel","-1")
    #line=line.replace("membership_PXrel","1")
    #print (line, end='')

def iggyvalidation():
  print('----------- [3] Run iggy + Validation (comparaison) -----------')
  #print('sh /home/computer/.local/bin/supmat/3-iggy/scripts/run-iggy.sh %s %s ${HOME}/.local/bin/supmat/1-diff-analysis/data/GSEA_EMThigh_vs_EMTlow_diffexp.csv 0 0' % (sys.argv[4], sys.argv[1]))
  #os.system('sh ./supmat/3-iggy/scripts/run-iggy.sh %s %s %s' % (ns.sif, ns.obs, ns.icgc))
  os.system('sh ./supmat/3-iggy/scripts/run-iggy.sh %s' %(ns.icgc))
def crossvalidation():
  print('----------- [4] Cross-Validation -----------')
  os.system('sh ./supmat/4-validation/scripts/run-validation.sh %s %s %s %s %s %s' % (ns.sif, ns.icgc, ns.start_sampling, ns.stop_sampling, ns.step_sampling, ns.numbers_run))

def plot():
  print('----------- [5] Run Plot -----------')
  os.system('sh ./supmat/5-plots/scripts/run-plots.sh')

if __name__ == '__main__':

  desc = ('This is a brief description of the pipeline')
  
  #parser = argparse.ArgumentParser(description=desc)

  
  #parser = argparse.ArgumentParser(description=desc, usage='python pipe.py [required arguments] [optional arguments]')

  #[LC_ALL=C] python3 pipe.py ErbB_signaling_pathway.sif roots.txt up 2345.obs

  #parser = optparse.OptionParser(description=desc, usage='Usage: python pipe.py networkfile nodefile upordown observationfile [options]')

  #optional = parser._action_groups.pop()
  #required = parser.add_argument_group('required arguments')

  

  #args = parser.parse_args()
  # Making sure all mandatory options appeared.
  #mandatories = ['network', 'nodes', 'updown', 'observations']
  #for m in mandatories:
    #if not opts.__dict__[m]:
      #print ("mandatory option is missing\n")
      #parser.print_help()
      #exit(-1)


  #arg[1] = le fichier sif/pathrider
  #arg[2] = le fichier roots (liste des noeuds)/pathrider
  #arg[3] = up or down
  #arg[4] = le fichier obs/iggy
  #arg[5] = le fichier ICGC


##def iggy():
  #print('----------- Run iggy -----------')

  #se positioner au dossier bin de iggy
  #param2 = 'python3 iggy.py %s %s' % ('/home/computer/.local/bin/supmat/2-graph-extraction/data/graph.sif', '/home/computer/.local/bin/supmat/3-iggy/data/2345.obs')
  #param2 = 'sh workflow-iggy.sh updownreg.obs graph.sif icgc-v4.csv 0 0'
  #os.system(param2)
  #s = '--help'
  #os.system('python3 iggy.py %s' % s)
  
  #os.system('sh workflow/run-validation.sh')
  #print(os.path.abspath(__file__))


parser = argparse.ArgumentParser(description='Pipeline HCC: require a file preceded by \'@\' and must contain all the required arguments cited below:',fromfile_prefix_chars='@', usage='Usage: python pipe.py @arguments_file [--steps]')

optional = parser.add_argument_group('optional arguments')
required = parser.add_argument_group('required arguments')


required.add_argument('--sif', help='influence graph in SIF format')
#required.add_argument('--root', help='the root nodes listed in a file (one node per line)')
#required.add_argument('--obs', help='observations file', required=True)
optional.add_argument('--dir', help='follows the up stream (\'up\') or the down stream (\'down\'). Default to \'up\'', default='up')
required.add_argument('--icgc', help='ICGC file')
required.add_argument('--b', help='a list of blacklisted genes (weakly expressed)')
optional.add_argument('--steps', type=str, default='1,2,3,4,5', help='specify the number of the steps to run:\n [1] Graph extraction\n [2] Pathrider\n [3] Iggy\n [4] Cross-Validation\n [5] Plots. (If many, separate by \',\'). Default run all steps')
optional.add_argument('--start_sampling', type=str, default='10', help='The start sampling percentage. Default= 10')
optional.add_argument('--stop_sampling', type=str, default='15', help='The stop sampling percentage. Default= 100')
optional.add_argument('--step_sampling', type=str, default='5', help='The step of sampling. Default= 5')
optional.add_argument('--numbers_run', type=str, default='2', help='The number of runs on each step. Default= 100')

ns = parser.parse_args()



if ns.steps :
  list_steps=ns.steps.split(',')


if '1' in ns.steps:
  diffanalysis()
if '2' in ns.steps:
  pathrider()
if '3' in ns.steps:
  iggyvalidation()
if '4' in ns.steps:
  crossvalidation()
if '5' in ns.steps:
  plot()

if '1' not in ns.steps and '2' not in ns.steps and '3' not in ns.steps and '4' not in ns.steps and '5' not in ns.steps:
  print('WARNING: Please enter a valid step number')


