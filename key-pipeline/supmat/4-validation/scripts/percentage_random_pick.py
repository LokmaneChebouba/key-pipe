# Library for the percentage random pick of observations
# ------------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret



import os
import math
import csv



# Global variables:
start = None    # Start of sampling range
stop = None     # End of sampling range
step = None     # Step of sampling range
values = None   # The range of sampling values
decimalPart = None    # Do the sampling values have a decimal part?
numExp = None   # Number of experiments for each sampling
expValues = None    # The range of experiment values
prefix = None   # Prefix of the sampling folders



def makeValues():
  """Create the range of sampling values"""
  global start, stop, step, decimalPart, values
  if values is not None:
    return values
  values = []   # Range of percentage values
  curVal = start   # Starting value
  decimalPart = False   # Is there at least one value with non-null decimal part?
  while curVal <= stop:
    if not 0.0 <= curVal <= 100.0:
      raise ValueError('This value is not a correct percentage: {}'.format(curVal))
    values.append(curVal)
    if math.modf(curVal)[0] != 0.0:
      decimalPart = True
    curVal += step
  return values

def makeExpValues():
  """Create the range of experiment values"""
  global numExp, expValues
  expValues = range(1, numExp + 1, 1)
  return expValues



def writeInfo(outDir):
  """Create and fill the info file in the main folder"""
  with open('{}/prp-info.csv'.format(outDir), 'w') as infoFile:
    infoFile.write('{}\t{}\t{}\t{}\t{}'.format(prefix, start, stop, step, numExp))

def dirInfo(dirName):
  """Load sampling info stored in the main folder"""
  global prefix, start, stop, step, numExp
  with open('{}/prp-info.csv'.format(dirName), 'r') as infoFile:
    dataReader = csv.reader(infoFile, delimiter='\t')
    row = next(dataReader)
  prefix = row[0]
  (start, stop, step) = (float(row[1]), float(row[2]), float(row[3]))
  numExp = int(row[4])

def loadInfo(dirName):
  """Load all info and returns the values and run values ranges"""
  dirInfo(dirName)
  return (makeValues(), makeExpValues())

def setInfo(argStart, argStop, argStep, argNumExp, argPrefix):
  """Sets info for a new experiment"""
  global start, stop, step, numExp, prefix
  (start, stop, step) = (float(argStart), float(argStop), float(argStep))
  numExp = int(argNumExp)
  prefix = str(argPrefix)



def nextDir(n, argPrevDir):
  """Compute the name of the next sampling directory"""
  global prefix, decimalPart
  # Current directory name: prpNNN or prpNNN.NNNNNNxxx...
  # with NNN the current percentage and x's if necessary
  prevDir = '' if argPrevDir is None else argPrevDir
  if not decimalPart:
    curDir = '{}{:03.0f}'.format(prefix, n)
  else:
    curDir = '{}{:08.4f}'.format(prefix, n)
    while curDir in prevDir:
      curDir += 'x'
  return curDir

def nextExpDir(i):
  """Compute the name of the next experiment folder"""
  global numExp
  return ('{:0' + str(len(str(numExp))) + 'd}').format(i)

def totalDir(dirName, curDir, curExpDir):
  """Compute the total directory address from the main folder, sampling and experiemnt names"""
  return '{}/{}/{}'.format(dirName, curDir, curExpDir)

