#!/bin/python3

# Library for scoring Iggy's predictions based on ICGC experimental data
# ----------------------------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive models: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret
###
# Library for scoring Iggy's predictions based on ICGC experimental data
###
# Matrix file syntax:
# Line 1: n values that are all inner bounds
# Line k: n + 2 values: 1 prediction type (+, -, 0, etc.) and n+1 scores
#           that correspond to values x ≤ n[0], n[0] < x ≤ n[1], etc.
#           => store score values as is for this prediction type
#     or: 3 values: 1 prediction type (+, -, 0, etc.), keyword 'cpy' or 'inv', and
#           another existing prediction type (+, -, 0, etc.)
#           => store identical or inverted values of first prediction
###



import csv
import bisect



# Empty matrix
scoreMatValues = None   # [List of bound values]
scoreMat = None   # Prediction type: [List of score values for each bound]

def checkMatrix():
  """Sanity check of the matrix and its bound values"""
  if scoreMatValues is None or scoreMat is None:
    raise ValueError('Matrix has not been loaded')
  if len(scoreMatValues) == 0:
    raise ValueError('scoreMatValues must contain values')
  if scoreMatValues != sorted(scoreMatValues):
    raise ValueError('scoreMatValues is not sorted')
  if len(scoreMatValues) != len(set(scoreMatValues)):
    raise ValueError('scoreMatValues has duplicates')
  if len(scoreMat) == 0:
    raise ValueError('Matrix must contain values')
  for r in scoreMat:
    if len(scoreMat[r]) != len(scoreMatValues) + 1:
      raise ValueError('Row {} of matrix has length {}, but length {} was expected'.format(r, len(scoreMat[r]), len(scoreMatValues) + 1))

def loadMatrix(f):
  """Load the matrix from file name f"""
  # Global variables
  global scoreMatValues
  global scoreMat
  scoreMat = {}
  # Keywords
  specialKeyWords = {
    'cpy': lambda l: l[:],
    'inv': lambda l: l[::-1] }
  
  # Open file
  with open(f, 'r') as fdata:
    dataReader = csv.reader(fdata, delimiter='\t')
    # First line: bouds
    row = next(dataReader)
    while row[0] == '': row.pop(0)
    scoreMatValues = list(map(float, row))
    # Next lines: prediction scores
    for row in dataReader:
      if len(row) > 0:
        # If special keyword...
        if row[1] in specialKeyWords.keys():
          scoreMat[row[0]] = specialKeyWords[row[1]](scoreMat[row[2]])
        # Without special keyword...
        else:
          scoreMat[row[0]] = list(map(float, row[1:]))
  checkMatrix()

def loadData(f):
  """Load prediction results + ICGC data from an ObsPred file named f"""
  genes = {}    # Gene name: (Gene prediction, Gene fold-change)
  with open(f, 'r') as fdata:
    dataReader = csv.reader(fdata, delimiter='\t')
    # Ignore first line
    next(dataReader)
    # Read (name, prediction, fold-change)
    for row in dataReader:
      (curName, curPred, curFC) = row[0:3]
      if curPred[0:5] == 'pred:' and curFC != 'not-found':
        genes[curName] = (curPred[5:], float(curFC))
  return genes

def findSegment(x):
  """Find segment of elemnt x in scoreMatValues"""
  if x > scoreMatValues[-1]:
    return len(scoreMatValues)
  else:
    return bisect.bisect_left(scoreMatValues, x)

def computeScore(genes):
  """Compute score of a given genes dictionary"""
  score = 0
  nbr = 0
  for g in genes:
    curIdx = findSegment(genes[g][1])
    curPred = genes[g][0]
    if curPred in scoreMat:
      score += scoreMat[curPred][curIdx]
      nbr += 1
  return score, nbr

def score(fMat, fPred):
  """General score function on files fMat (matrix) and fPred (Iggy predictions and ICGC data)"""
  if scoreMat is None:
    loadMatrix(fMat)
  s, l = computeScore(loadData(fPred))
  return s / l if l != 0 else 0

def score_nn(fMat, fPred):
  """General score function on files fMat (matrix) and fPred (Iggy predictions and ICGC data),
  without normalization"""
  if scoreMat is None:
    loadMatrix(fMat)
  return computeScore(loadData(fPred))[0]

## DEBUG
#def printMatrix():
#  """Print matrix"""
#  print(scoreMatValues)
#  for k in scoreMat:
#    print('{:>6}: {}'.format(k, scoreMat[k]))

