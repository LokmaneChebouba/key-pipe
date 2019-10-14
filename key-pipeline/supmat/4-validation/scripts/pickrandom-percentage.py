#!/bin/python3
#coding=utf-8

# Cross-validation based on a random pick of a given percentage of observations
# -----------------------------------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive functional networks: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret
###
# Cross-validation based on a random pick of a given percentage of observations
###
# Help:
#   python pickrandom-percentage.py --help
#
# Bash scripts required:
# - construct-inputs.sh
#   - extract-inputs.sh
###



import os
import subprocess
import random
import argparse
import percentage_random_pick as prp
import util



# DEBUG
# Fake shell call + error code handling
#def shellCall(c, grep = None):
#  print(c)

# Shell call + error code handling
# Arguments:
#   c : command to be executed by the shell (str)
#   grep : consider exit code 1 as not an error (bool; default = try to infer from c)
def shellCall(c, grep = None):
  if grep is None:
    erGrep = c[0:4] == 'grep'
  else:
    erGrep = grep
  retValue = subprocess.call(c, shell = True)
  if ((not erGrep) and (retValue > 0)) or (erGrep and (retValue > 1)):
    raise Exception('Something went wrong with command:\n$ {}'.format(c))



# [Argparse] Command line parsing options
parser = argparse.ArgumentParser(
  add_help = False,
  description = """Cross-validation based on a random pick of a given percentage of observations.""",
  epilog = """The program uses a counter x which ranges from START to STOP and increses of STEP.
    At each turn, it takes x% of the up-regulated and x% of the down-regulated genes
    and considers them as observations for Iggy.
    Statistics on the results can be computed with the other scripts names stats-*.py.
    ICGCFILE should be a tab-delimited CSV file containing in its first two columns
    the gene names and their fold-change values, sorted by fold-change (decreasing).
    UPOBS and DOWNOBS should be two lists of gene names (with one name per line).""")

parser.add_argument('sifFileName', metavar = 'SIFFILE', type = str,
  help = 'The SIF file containing the graph')
parser.add_argument('dataFileName', metavar = 'DATAFILE', type = str,
  help = 'The CSV file containing (ICGC) expression data')
parser.add_argument('upFileName', metavar = 'UPOBS', type = str,
  help = 'The list of all up-regulated observation genes')
parser.add_argument('downFileName', metavar = 'DOWNOBS', type = str,
  help = 'The list of all down-regulated observation genes')
parser.add_argument('cvStart', metavar = 'START', type = float,
  help = 'The starting value of the counter')
parser.add_argument('cvStop', metavar = 'STOP', type = float,
  help = 'The ending value of the counter')
parser.add_argument('cvStep', metavar = 'STEP', type = float,
  help = 'The step of the counter')
parser.add_argument('numExp', metavar = 'NBR', type = int,
  help = 'Run NBR experiments for each turn')
parser.add_argument('outDir', metavar = 'OUTDIR', type = str,
  help = 'The directoy to write the experiments to')
parser.add_argument('-s', '--scripts-path', dest = 'scriptsPath',
  metavar = 'PATH', type = str, action = 'store', default = util.defaultIggyDir(),
  help = 'Specify a path for the Shell and Python scripts (default: ../Iggy)')
parser.add_argument('-c', '--iggy-command', dest = 'iggyCommand',
  metavar = 'IGGY', type = str, action = 'store', default = 'iggy',
  help = 'Specify a command to call Iggy (default: iggy)')
parser.add_argument('--continue', dest = 'newDir', action = 'store_false',
  help = 'Don\'t create OUTDIR; useful to carry on a started computation')
parser.add_argument('-h', '--help', action = 'help',
  help = 'Print this help message')

args = parser.parse_args()



# Iggy's directory (where all the scripts are) and command
iggyDir = args.scriptsPath
iggyCommand = args.iggyCommand

# Set info and create range of sampling values
prp.setInfo(args.cvStart, args.cvStop, args.cvStep, args.numExp, 'prp')
values = prp.makeValues()
expValues = prp.makeExpValues()



# Output directories
outDir = args.outDir    # Working directory for outputs
if outDir[-1:] == '/': outDir = outDir[:-1]
curDir = None    # Directory for current percentage (n)
curExpDir = None    # Directory for current experiment
totCurDir = None   # Complete current directory (outDir + curDir + curExpDir)

# Create directory
if args.newDir:
  os.makedirs(outDir)
  prp.writeInfo(outDir)



# Open and parse the lists of observations
geneNames = util.loadGeneNames([args.upFileName, args.downFileName])

# Need to handle the _gen suffix?
genFlag = '--gen' if geneNames[0][0][-4:] == '_gen' else ''



# For each percentage value...
# n = current percentage; k = current sample sizes (n% of all up- and down-regulated genes)
for n in values:
  k = [round(n / 100.0 * len(geneNames[upDown])) for upDown in [0, 1]]
  curDir = prp.nextDir(n, curDir)
  print(curDir)
  os.makedirs('{}/{}'.format(outDir, curDir))
  # For each expriment...
  for i in expValues:
    curExpDir = prp.nextExpDir(i)
    totCurDir = prp.totalDir(outDir, curDir, curExpDir)    # Complete directory
    print('  -- {}'.format(curExpDir), end='')
    os.makedirs(totCurDir)
    # Pick and write current observations
    selectedGenes = [random.sample(geneNames[upDown], k[upDown]) for upDown in [0, 1]]
    with open('{}/obs-noinputs.obs'.format(totCurDir), 'w') as obsFile:
      for upDown in [0, 1]:
        for gn in selectedGenes[upDown]:
          obsFile.write('{} = {}\n'.format(gn, '+' if upDown == 0 else '-'))
  
    # Construct inputs
    shellCall('sh {}/construct-inputs.sh "{}" "{}/obs-noinputs.obs" > "{}/obs-withinputs.obs"'.format(iggyDir, args.sifFileName, totCurDir, totCurDir))
    # Call Iggy
#    os.makedirs(totCurDir)
    shellCall('sh {}/workflow-iggy.sh {} --iggy-command "{}" "{}/obs-withinputs.obs" "{}" "{}" 0 0 "{}/iggy-output.out" > "{}/result-0.0.tsv"'.format(iggyDir, genFlag, iggyCommand, totCurDir, args.sifFileName, args.dataFileName, totCurDir, totCurDir))
  
    # End of current run
    print()
  
  # End of current sampling (n%)

# End of the world

print('Done.')

