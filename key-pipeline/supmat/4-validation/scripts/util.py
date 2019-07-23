# General-purpose library for statistical validation
# --------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# Hepatocellular carcinoma computational models identify key protein-complexes associated to tumor progression
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret



import os
import csv



def defaultIggyDir():
  """Return the relative path to the scripts related to Iggy"""
  # Computed from the absolute path to the directory of this script
  return '{}/../Iggy'.format(os.path.dirname(os.path.abspath(__file__)))



def removeLastSlash(curDir):
  """Remove trailing slash from a path name"""
  return curDir[:-1] if curDir[-1:] == '/' else curDir

def hasProperResult(testDir):
  """Check if a folder contains a proper Iggy result, based on NORESULT files"""
  NoResultFileName = '{}/NORESULT'.format(removeLastSlash(testDir))
  return not os.path.isfile(NoResultFileName)

def old_hasProperResult(testDir):
  """Check if a folder contains a proper Iggy result - OLD VERSION"""
  iggyOutputFileName = '{}/iggy-output.out'.format(removeLastSlash(testDir))
  res = False
  # The file iggy-output.out must exist
  if os.path.isfile(iggyOutputFileName):
    # The file iggy-output.out must not be empty
    res = os.stat(iggyOutputFileName).st_size != 0
  return res



def loadGeneNames(argInFileNames):
  """Open and parse one or several list(s) of gene names (such as observations)"""
  inFileNames = [argInFileNames] if type(argInFileNames) == str else argInFileNames
  geneNames = []   # List of lists of strings (gene names)
  for fileNum in range(len(inFileNames)):
    geneNames.append([])
    with open(inFileNames[fileNum], 'r') as fdata:
      dataReader = csv.reader(fdata, delimiter='\t')
      for row in dataReader:
        if row[0] != '':
          geneNames[fileNum].append(row[0])
  if type(argInFileNames) == str:
    geneNames = geneNames[0]
  return geneNames

def loadCSV(fileName, convert = None, skip = 0):
  """Load and return the content of a CSV file, excluding first line, with obtional conversions"""
  res = []
  with open(fileName, 'r') as curFile:
    dataReader = csv.reader(curFile, delimiter='\t')
    # Skip head lines
    for _ in range(skip):
      next(dataReader)
    # Read lines
    for row in dataReader:
      res.append(row[:])
  if convert is None:
    return res
  else:
    maxrow = max(len(row) for row in res)
    # Complete conversion list
    filledConvert = [convert[i] if i < len(convert) else str for i in range(maxrow)]
    # Perform conversion and return
    return [[filledConvert[i](row[i]) for i, _ in enumerate(row)] for row in res]

def loadCSVWithHeader(fileName, convert = None):
  return loadCSV(fileName, convert = convert, skip = 1)

