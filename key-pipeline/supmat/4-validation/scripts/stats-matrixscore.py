#!/bin/python3
#coding=utf-8

# Compute matrix scores on random pick cross-validation results
# -------------------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# A pipeline to create predictive functional networks: application to the tumor progression of hepatocellular carcinoma
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

###
# Compute matrix scores on random pick cross-validation results
###
# Help:
#   python stats-matrixscore.py --help
#
# Example:
#   python stats-matrixscore.py prp-10-95-5-100/ m2.tsv --detail-scores --complete-pred "result.tsv" --export-plot --verbose
###



import os
import sys
import math
import csv
import argparse
import scorematrix
import statistics
import percentage_random_pick as prp
import util



# [Argparse] Command line parsing options
parser = argparse.ArgumentParser(
  add_help = False,
  description = """Compute matrix scores on random pick cross-validation results.""",
  epilog = """The program takes a result folder of the random pick cross-validation script
    and computes independent scores based on a given score matrix,
    and then computes global mean and deviation for each sampling.""")

parser.add_argument('dirName', metavar = 'DIRNAME', type = str,
  help = 'The directory containing the result of the cross-validation computation')
parser.add_argument('matFileName', metavar = 'MATFILE', type = str,
  help = 'The file containing the score matrix')

parser.add_argument('--detail-scores', dest = 'detailScores', action = 'store_true',
  help = 'Print the score of each individual run')
parser.add_argument('--do-not-normalize', dest = 'noNormalization', action = 'store_true',
  help = 'Do not normalize the scores on the number of predictions')

parser.add_argument('-p', '--export-plot', dest = 'plot', action = 'store_true',
  help = 'Generate a boxplot from the scores')
parser.add_argument('-i', '--export-image', dest = 'image', action = 'store_true',
  help = 'Export a PNG image of the boxplot')
parser.add_argument('-c', '--complete-pred', dest = 'predFileName',
  metavar = 'PREDFILE', type = str, action = 'store',
  help = 'The complete predictions to add at the end of the plot')
parser.add_argument('-pdf', '--pdf', dest = 'imagePDF', action = 'store_true',
  help = 'Export a PDF image of the boxplot')
parser.add_argument('-d', '--dest-plot', dest = 'destPlotName',
  metavar = 'DESTPLOT', type = str, action = 'store', default = '',
  help = 'The destination of the plot files (HTML, JPG, PDF) relative to DIRNAME')

parser.add_argument('-m', '--plot-mean-pred', dest = 'plotPred', action = 'store_true',
  help = 'Add mean number of predictions to the plot')
parser.add_argument('-mmm', '--plot-mmm-pred', dest = 'plotMMMPred', action = 'store_true',
  help = 'Add mean, min and max number of predictions to the plot')

parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true',
  help = 'Print computation steps information on the standard output')

parser.add_argument('-h', '--help', action = 'help',
  help = 'Print this help message')

args = parser.parse_args()

if args.plot is False and args.image is True:
  print('Arguments error: Options --export-image requires --export-plot', file = sys.stderr)
  exit()
if args.plot is False and args.predFileName is not None:
  print('Arguments error: Options --complete-pred requires --export-plot', file = sys.stderr)
  exit()
if args.plot is False and args.plotPred is True:
  print('Arguments error: Options --plot-mean-pred requires --export-plot', file = sys.stderr)
  exit()
if args.plot is False and args.plotMMMPred is True:
  print('Arguments error: Options --plot-mmm-pred requires --export-plot', file = sys.stderr)
  exit()



if args.verbose:
  print('Begin.')

# Output directories
dirName = util.removeLastSlash(args.dirName)    # Working directory for outputs
destPlotName = args.destPlotName    # Output directory for plots
if destPlotName != '' and destPlotName[0] != '/': destPlotName = '/' + destPlotName
curDir = None    # Directory for current percentage (n)
curExpDir = None    # Directory for current experiment
totCurDir = None   # Complete current directory (dirName + curDir + curExpDir)

# Matrix name
matName = os.path.splitext(os.path.basename(args.matFileName))[0]

# Score function
f_score = scorematrix.score_nn if args.noNormalization else scorematrix.score

# Load info
values, expValues = prp.loadInfo(dirName)

# Initialize empty plot and data
if args.plot or args.imagePDF:
  import plotly.offline as pl
  import plotly.graph_objs as go
  plotData = []
  predMeanList = []
  predMaxList = []
  predMinList = []



if args.verbose:
  print('Gather data and compute scores...')

# For each percentage value...
# n = current percentage
for n in values:
#  prevDir = curDir    # Previous directory name
#  totPrevDir = totCurDir    # Previous total directory
  scoresList = []   # List of score matrix scores
  numPredList = []  # List of prediction numbers
  curDir = prp.nextDir(n, curDir)
  if args.verbose or args.detailScores:
    print(curDir, end = '\n' if args.detailScores else ': ')
  # For each expriment...
  for i in expValues:
    curExpDir = prp.nextExpDir(i)
    totCurDir = prp.totalDir(dirName, curDir, curExpDir)    # Complete current directory
    if util.hasProperResult(totCurDir):
      # Compute score
      score = f_score(args.matFileName, '{}/result-0.0.tsv'.format(totCurDir))
      scoresList.append(score)
      # Compute number of predictions
      dataRes = util.loadCSV('{}/result-0.0.tsv'.format(totCurDir), skip = 1)
      numPred = len([row for row in dataRes if row[1][0:5] == 'pred:'])
      numPredList.append(numPred)
      with open('{}/score-{}.txt'.format(totCurDir, matName), 'w') as matFile:
        matFile.write(str(score))
      if args.detailScores:
        print('  -- {}: score = {}'.format(curExpDir, score))
  
  # End of current sampling (n%)
  if args.verbose:
    print('mean = {:.4f}, SD = {:.4f}, mean #pred = {}'.format(statistics.mean(scoresList),
      statistics.pstdev(scoresList), statistics.mean(numPredList)))
  
  # Create current box and data for the plot
  if args.plot or args.imagePDF:
    predMeanList.append(statistics.mean(numPredList))
    predMaxList.append(max(numPredList))
    predMinList.append(min(numPredList))
    plotData.append(go.Box(
      name = ('{:0.0f}%' if not prp.decimalPart else '{:0.4f}%').format(n),
      x = [n] * len(scoresList),
      y = scoresList[:],
      boxpoints = 'outliers' if args.imagePDF else 'all',
#      jitter = 0.3,
      pointpos = 0 if args.imagePDF else -1.8
#      boxmean='sd'
    ))

# End of the world

# Show box plots of scores and line plots of number of predictions
if args.plot or args.imagePDF:
  plotFileName = '{}{}/{}-mean-boxplot{}'.format(dirName, destPlotName, matName, '-nn' if args.noNormalization else '')
  if args.verbose:
    print('Build plot ({})...'.format(plotFileName))
  plotValues = values[:]
  # Add last point at 100% sampling
  if args.predFileName is not None:
    plotValues += [100]
    totPred = len([row for row in util.loadCSVWithHeader(args.predFileName)
        if row[1][0:5] == 'pred:'])
    predMeanList.append(totPred)
    predMaxList.append(totPred)
    predMinList.append(totPred)
    plotData.append(go.Scatter(
      name = ('{:0.0f}' if not prp.decimalPart else '{:0.4f}').format(100),
      x = [100],
      y = [f_score(args.matFileName, args.predFileName)],
#      boxpoints = 'outliers' if args.imagePDF else 'all',
#      jitter = 0.3,
#      pointpos = -1.8
#      boxmean='sd'
    ))
  # Add number of predictions (min, max, mean)
  if args.plotPred or args.plotMMMPred:
    # Mean
    plotData.append(go.Scatter(
      x = plotValues,
      y = predMeanList,
      yaxis = 'y2',
      mode = 'lines+markers',
      line = dict(
        color = 'blue'
      ),
      name = 'Mean # pred'
    ))
  if args.plotMMMPred:
    # Max
    plotData.append(go.Scatter(
      x = plotValues,
      y = predMaxList,
      yaxis = 'y2',
      mode = 'lines+markers',
      line = dict(
        color = 'green'
      ),
      name = 'Max # pred'
    ))
    # Min
    plotData.append(go.Scatter(
      x = plotValues,
      y = predMinList,
      yaxis = 'y2',
      mode = 'lines+markers',
      line = dict(
        color = 'red'
      ),
      name = 'Min # pred'
    ))
  # Layout
  plotLayout = go.Layout(
    title = 'Boxplot of the precision scores for each sampling',
    showlegend = False,
    xaxis = dict(
      title = 'Sampling (%)',
    ),
    yaxis = dict(
#      range = [0, 1],
      title = 'Score'
    )
  )
  if args.plotMMMPred:
    plotLayout['title'] += '& mean, min and max number of predictions'
  elif args.plotPred:
    plotLayout['title'] += '& mean number of predictions'
  if args.plotPred or args.plotMMMPred:
    plotLayout['yaxis2'] = dict(
      autorange = True,
      overlaying = 'y',
      side = 'right',
      rangemode = "tozero", # "nonnegative",
      title = 'Number of predictions'
    )
  # Build plot
  plotFig = go.Figure(data = plotData, layout = plotLayout)
  if args.imagePDF:
    import plotly.io
    plotly.io.write_image(plotFig, plotFileName + '.pdf')
  if args.plot:
    if not args.image:
      pl.plot(plotFig, filename = plotFileName + '.html', show_link = False)
    else:
      pl.offline.plot(plotFig, filename = plotFileName + '_img.html', show_link = False,
        image = 'png', image_width = 1600, image_height = 1200, image_filename = plotFileName)
      pl.plot(plotFig, filename = plotFileName + '.html', show_link = False, auto_open = False)

if args.verbose:
  print('Done.')

