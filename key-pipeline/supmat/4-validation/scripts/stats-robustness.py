#!/bin/python3
#coding=utf-8

# Compute robustness statistics on the result of the random pick cross-validation
# -------------------------------------------------------------------------------
# This file is part of the Supplementary Material of the submission entitled:
# Hepatocellular carcinoma computational models identify key protein-complexes associated to tumor progression
# Authors: Maxime Folschette, Vincent Legagneux, Arnaud Poret, Lokmane Chebouba, Carito Guziolowski and Nathalie Théret

###
# Compute robustness statistics on the result of the random pick cross-validation
###
# Help:
#   python stats-robustness.py --help
#
# Example:
#   python stats-robustness.py prp-10-95-5-100/ out.tsv --complete-pred "result.tsv" --brief-weak --sum-all --verbose -ncp -100
###



import os
import sys
import argparse
import statistics
import percentage_random_pick as prp
import util



# [Argparse] Command line parsing options
parser = argparse.ArgumentParser(
  add_help = False,
  description = """Compute robustness statistics on the result of the random pick cross-validation.""",
  epilog = """The program takes a result folder of the random pick cross-validation script
    and gathers all prediction results in a CSV file for robustness check purposes.
    The folder must contain a file named 'prp-info.csv' that contains the information
    about the cross-validation.""")

parser.add_argument('dirName', metavar = 'DIRNAME', type = str,
  help = 'The directory containing the result of the cross-validation computation')
parser.add_argument('outFileName', metavar = 'OUTFILE', type = str,
  help = 'The file to write the results to')

parser.add_argument('--complete-pred', dest = 'predFileName',
  metavar = 'PREDFILE', type = str, action = 'store',
  help = 'The complete predictions to add at the end of the file, for comparison')
parser.add_argument('--sum-from', dest = 'sumFrom',
  metavar = 'N', nargs = '+', type = float, action = 'store',
  help = """Show percentage of good/bad/missing predictions starting from sampling N;
    requires --complete-pred""")
parser.add_argument('--sum-all', dest = 'sumAll', action = 'store_true',
  help = """Show percentage of good/bad/missing predictions for all samplings;
    requires --complete-pred""")
parser.add_argument('--brief-weak', dest = 'briefWeak', action = 'store_true',
  help = 'Shrink weak predictions in one only column')
parser.add_argument('--detail-sum', dest = 'detailSum', action = 'store_true',
  help = 'Give original values of the sum percentages')
parser.add_argument('--bad-weak', dest = 'goodWeak', action = 'store_false',
  help = 'Count weak predictions as always bad compared to strong predictions')
#parser.add_argument('-x', '--exclude-pred', dest = 'excludePred',
#  metavar = 'PRED', nargs = '+', type = str, action = 'store', default = [],
#  help = 'Exclude these predictions from the result')

parser.add_argument('-ncp', '--noncumulative-plot', dest = 'exportNCPlot', action = 'store_true',
  help = 'Export a plot of the good/bad/missing statistics for each sampling')
parser.add_argument('-cp', '--cumulative-plot', dest = 'exportCPlot', action = 'store_true',
  help = 'Export a plot of the cumulative good/bad/missing statistics')
parser.add_argument('-i', '--export-image', dest = 'image', action = 'store_true',
  help = 'Exports a PNG image of the plot')
parser.add_argument('-100', '--final-point', dest = 'finalPoint', action = 'store_true',
  help = 'Extends the curves to the final 100%% sampling')
parser.add_argument('-pdf', '--pdf', dest = 'imagePDF', action = 'store_true',
  help = 'Export instead a PDF image of the plot')
parser.add_argument('-d', '--dest-plot', dest = 'destPlotName',
  metavar = 'DESTPLOT', type = str, action = 'store', default = '',
  help = 'The destination of the plot files (HTML, JPG, PDF) relative to DIRNAME')

parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true',
  help = 'Print computation steps information on the standard output')

parser.add_argument('-h', '--help', action = 'help',
  help = 'Print this help message')

args = parser.parse_args()

# Check arguments
if args.sumAll is True and args.sumFrom is not None:
  print('Arguments error: Options --sum-from and --sum-all are incompatible', file = sys.stderr)
  exit()
if args.sumFrom is not None and args.predFileName is None:
  print('Arguments error: Option --sum-from requires --complete-pred', file = sys.stderr)
  exit()
if args.sumAll is True and args.predFileName is None:
  print('Arguments error: Option --sum-all requires --complete-pred', file = sys.stderr)
  exit()
if args.exportCPlot is True and args.exportNCPlot is True:
  print('Arguments error: Options --cumulative-plot and --noncumulative-plot are incompatible', file = sys.stderr)
  exit()
if args.exportCPlot is True and (args.sumAll is False and args.sumFrom is None):
  print('Arguments error: Option --cumulative-plot requires --sum-from or --sum-all', file = sys.stderr)
if args.finalPoint is True and (args.exportCPlot is False and args.exportNCPlot is False):
  print('Arguments error: Option --final-point requires --cumulative-plot or --noncumulative-plot', file = sys.stderr)
  exit()
if args.imagePDF is True and (args.exportCPlot is False and args.exportNCPlot is False):
  print('Arguments error: Option --pdf requires --cumulative-plot or --noncumulative-plot', file = sys.stderr)
  exit()



if args.verbose:
  print('Begin.')

# Directories
dirName = util.removeLastSlash(args.dirName)
destPlotName = args.destPlotName    # Output directory for plots
if destPlotName != '' and destPlotName[0] != '/': destPlotName = '/' + destPlotName
curDir = None    # Directory for current percentage (n)
curExpDir = None    # Directory for current experiment
totCurDir = None   # Complete current directory (dirName + curDir + curExpDir)

# Load info
values, expValues = prp.loadInfo(dirName)
values.sort()

sumFrom = None
if args.sumFrom is not None:
  sumFrom = args.sumFrom
elif args.sumAll:
  sumFrom = values



# Initializing
# geneStats structure: n% values dictionary / gene dictionary / predType index dictionary / count int
geneStats = {}
geneStatsList = []
if not args.briefWeak:
  geneStatsPredTypes = [
    (['+'], '+'),
    (['-'], '−'),
    (['0'], '0'),
    (['NOT+'], 'NOT+'),
    (['NOT-'], 'NOT−'),
    (['CHANGE'], 'CHANGE')]
else:
  geneStatsPredTypes = [
    (['+'], '+'),
    (['-'], '−'),
    (['0'], '0'),
    (['NOT+', 'NOT-', 'CHANGE'], 'weak')]
  if args.goodWeak:
    weakPredTypes = {
      'NOT+': ['+', '0'],
      'NOT-': ['-', '0'],
      'CHANGE': ['+', '-']}
geneStatsPredTypesFlat = sum(list(zip(*geneStatsPredTypes))[0], [])
trueNumExp = {}   # True number of experiments for each sampling (excludes failes ones)
cumulativeTrueNumExp = {}   # Idem with descending accumulation on values of sumFrom

# Find corresponding index in the list of sought predictions
def findPredIndex(pred):
  return next(i for i, v in enumerate(geneStatsPredTypes) if pred in v[0])



# If required, load the complete predictions file (i.e. 100% sampling)
if args.predFileName is not None or args.exportNCPlot:
  if args.verbose:
    print('Load complete predictions file ({})...'.format(args.predFileName))
  # Dict of final predictions (100% sampling)
  completeGenePred = {}
  # (Non-)cumulative statistics: number of good/bad predictions starting from each sampling value
  if args.exportNCPlot:
    # nonCumulativeGeneStats structure: nn dict / gene dict / 'good' int, 'bad' int
    nonCumulativeGeneStats = {}
  if args.predFileName is not None:
    # cumulativeGeneStats structure: gene dict / nn dict / 'good' int, 'bad' int
    cumulativeGeneStats = {}
  for row in util.loadCSVWithHeader(args.predFileName):
    curGene = row[0]
    curPred = row[1]
    curPredType = curPred[5:]
    if curPred[:5] == 'pred:' and curPredType in geneStatsPredTypesFlat:
#      cumulativeGeneStats[curGene] = {'pred': curPredType}
      completeGenePred[curGene] = curPredType
      if sumFrom is not None:
        cumulativeGeneStats[curGene] = {}
        for nn in sumFrom:
          cumulativeGeneStats[curGene][nn] = {'good': 0, 'bad': 0}

if args.exportNCPlot:
  for n in values:
    nonCumulativeGeneStats[n] = {}
    for curGene in completeGenePred:
      nonCumulativeGeneStats[n][curGene] = {'good': 0, 'bad': 0}



# Gather data in each experiment
if args.verbose:
  print('Gather data on all runs...')

# For each percentage value... n = current percentage
for n in values:
  trueNumExp[n] = 0
  curDir = prp.nextDir(n, curDir)
  if args.verbose:
    print('  {}'.format(curDir))
  # For each expriment...
  for i in expValues:
    curExpDir = prp.nextExpDir(i)
    totCurDir = prp.totalDir(dirName, curDir, curExpDir)    # Complete current directory
    # Gather predictions
    if n not in geneStats:
      geneStats[n] = {}
    if util.hasProperResult(totCurDir):
      trueNumExp[n] += 1
      for row in util.loadCSVWithHeader('{}/result-0.0.tsv'.format(totCurDir)):
        curGene = row[0]
        curPred = row[1]
        curPredType = curPred[5:]
        if curPred[:5] == 'pred:' and curPredType in geneStatsPredTypesFlat:
          # Find index in geneStatsPredTypes
          curPredIndex = findPredIndex(curPredType)
          # Add gene to geneStats[n]
          if curGene not in geneStats[n]:
            geneStats[n][curGene] = {}
            # Add gene to geneStatsList
            if curGene not in geneStatsList:
              geneStatsList.append(curGene)
          # Add prediction to geneStats[n][curGene]
          if curPredIndex not in geneStats[n][curGene]:
            geneStats[n][curGene][curPredIndex] = 0
          geneStats[n][curGene][curPredIndex] += 1
          # If current gene is in final predictions
          if curGene in completeGenePred:
            goodBad = curPredType == completeGenePred[curGene]
            if args.goodWeak and curPredType in weakPredTypes:
              goodBad = completeGenePred[curGene] in weakPredTypes[curPredType]
            # Non-cumulative statistics to compare with complete predictions
            if args.exportNCPlot:
              nonCumulativeGeneStats[n][curGene]['good' if goodBad else 'bad'] += 1
            # Cumulative statistics to compare with complete predictions
            if sumFrom is not None:
              for nn in sumFrom:
                if n >= nn:
                  cumulativeGeneStats[curGene][nn]['good' if goodBad else 'bad'] += 1
  # End of current sampling (n%)

# Compute cumulative true number of experiments (with proper results)
if sumFrom is not None:
  cumulativeTrueNumExp = {n: sum([trueNumExp[nn] for nn in trueNumExp if nn >= n]) for n in sumFrom}
#cumulativeTrueNumExpValues = {n: sum([trueNumExp[nn] for nn in trueNumExp if nn >= n]) for n in values}



# End of loop: write final output file
totalOutFileName = '{}/{}'.format(dirName, args.outFileName)

if args.verbose:
  print('Write results in output file ({})...'.format(totalOutFileName))

with open(totalOutFileName, 'w') as statsFile:
  # First head line
  curLine = 'sampling (%)'
  for n in values:
    curLine += '\t{}'.format(n) + ('\t' * (len(geneStatsPredTypes) - 1))
  if args.predFileName is not None:
    curLine += '\tfinal (100)'
    if sumFrom is not None:
      for nn in sumFrom:
        curLine += '\t\tsum ≥ {}%\t\t'.format(nn)
  statsFile.write(curLine + '\n')
  # Second head line
  curLine = ''
  for p in geneStatsPredTypes:
    curLine += '\t' + p[1]
  curLine *= len(values)
  curLine = 'prediction' + curLine
  if args.predFileName is not None:
    curLine += '\tprediction'
    if sumFrom is not None:
      for nn in sumFrom:
        curLine += '\t\tgood\tbad\tmissing'
  statsFile.write(curLine + '\n')
  # Content
  for curGene in geneStatsList:
    curLine = curGene
    for n in values:
      if curGene not in geneStats[n]:
        curLine += '\t' * len(geneStatsPredTypes)
      else:
        for curPredIndex, curPred in enumerate(geneStatsPredTypes):
          curLine += '\t'
          if curPredIndex in geneStats[n][curGene]:
            curLine += str(geneStats[n][curGene][curPredIndex])
    # If the complete predictions file is provided: add the final predictions
    if args.predFileName is not None:
      curLine += '\t'
      if curGene in completeGenePred:
        c = findPredIndex(completeGenePred[curGene])
        curLine += geneStatsPredTypes[c][1]
        if len(geneStatsPredTypes[c][0]) > 1:
          curLine += ' ({})'.format(completeGenePred[curGene])
        # If cumulative statistics are required
        if sumFrom is not None:
          for nn in sumFrom:
            curGood = cumulativeGeneStats[curGene][nn]['good']
            curBad = cumulativeGeneStats[curGene][nn]['bad']
            curTot = cumulativeTrueNumExp[nn]
            curMissing = curTot - (curGood + curBad)
#            curMissing = ((prp.numExp * len([nnn for nnn in values if nnn >= nn])) -
#              (cumulativeGeneStats[curGene][nn]['good'] + cumulativeGeneStats[curGene][nn]['bad']))
#            curTot = curGood + curBad + curMissing
            if not args.detailSum:
              curLine += '\t' + ('\t{}' * 3).format(curGood / curTot,
                curBad / curTot, curMissing / curTot)
            else:
              curLine += '\t' + ('\t{} ({}/{})' * 3).format(curGood / curTot, curGood, curTot,
                curBad / curTot, curBad, curTot, curMissing / curTot, curMissing, curTot)
    statsFile.write(curLine + '\n')



# Build the plot
if args.exportCPlot or args.exportNCPlot:
  plotFileName = '{}{}/{}'.format(dirName, destPlotName, os.path.splitext(os.path.basename(args.outFileName))[0])
  plotValues = values if args.exportNCPlot else sumFrom
  if args.verbose:
    print('Build plot ({}.html)...'.format(plotFileName))
  import plotly.offline as pl
  import plotly.graph_objs as go
  # List of values to consider (number of good, bad and missing predictions)
  keysList = [('good', (0, 1, 0)), ('bad', (1, 0, 0)), ('missing', (0, 0, 1))]
  # Fonctions to plot (min, max, mean and median)
  functionsList = [   # (function, name, brightness, opacity, fill type, marker)
    (min, 'Min', 0.33, .3, 'none', 'circle-open'),
    (max, 'Max', 1.0, .3, 'tonexty', 'circle-open'),
    (statistics.mean, 'Mean', 0.66, 1, 'none', 'square'),
    (statistics.median, 'Median', 0.66, 1, 'tonexty', 'diamond')]
  plotStats = {}  # 'good','bad','missing' dict / int list
  plotData = {}   # 'good','bad','missing' dict / function dict / int list
  for k in keysList:
    plotData[k[0]] = {}
    for f in functionsList:
      plotData[k[0]][f[1]] = []
  # TODO: Fix the cumulative version
  # Gather data for (non-)cumulative plot
  if args.exportNCPlot:
    for nn in plotValues:
      if args.exportNCPlot:
        curN = nonCumulativeGeneStats[nn]
        totExpLeft = trueNumExp[nn]
        plotStats['good'] = [g['good'] for g in curN.values()]
        plotStats['bad'] = [g['bad'] for g in curN.values()]
      elif args.exportCPlot:
        curN = [g[nn] for g in cumulativeGeneStats.values()]
        totExpLeft = cumulativeTrueNumExp[nn]
        plotStats['good'] = [g['good'] for g in curN]
        plotStats['bad'] = [g['bad'] for g in curN]
      plotStats['missing'] = [totExpLeft -
        (numGood + numBad) for numGood, numBad in zip(plotStats['good'], plotStats['bad'])]
      for k in keysList:
        for f in functionsList:
          plotData[k[0]][f[1]].append(f[0](plotStats[k[0]]) / totExpLeft * 100)
  # Add final abscissa point
  plotValues.append(100)
  # Build plots
  allPlots = []
  for k in keysList:
    for f in functionsList:
      # Add final ordinates point
      if args.finalPoint:
        plotData[k[0]][f[1]].append(100 if k[0] == 'good' else 0)
      allPlots.append(go.Scatter(
        x = plotValues,
        y = plotData[k[0]][f[1]],
        mode = 'lines+markers',
        fill = f[4],
        fillcolor = 'rgba({}, {}, {}, {})'.format(*[c * f[2] * 255 for c in k[1]], .1),
        line = dict(
          color = 'rgba({}, {}, {}, {})'.format(*[c * f[2] * 255 for c in k[1]], f[3])
        ),
        marker = dict(
          symbol = f[5]
        ),
        name = '{} {}'.format(f[1], k[0])
      ))
  plotLayout = go.Layout(
    title = '{}volution of max, min, mean and median of{}good, bad and missing predictions compared to 100% sampling'.format('E' if args.exportNCPlot else 'Cumulative e', '<br />' if args.imagePDF else ' '),
    showlegend = True,
    xaxis = dict(
      title = 'Sampling (%)'
    ),
    yaxis = dict(
      title = 'Number of good/bad/missing predictions (%)'
    )
  )
  plotFig = go.Figure(data = allPlots, layout = plotLayout)
  if args.imagePDF:
    import plotly.io
    plotly.io.write_image(plotFig, plotFileName + '.pdf')
  else:
    if not args.image:
      pl.plot(plotFig, filename = plotFileName + '.html', show_link = False)
    else:
      pl.offline.plot(plotFig, filename = plotFileName + '_img.html', show_link = False,
        image = 'png', image_width = 1600, image_height = 1200, image_filename = plotFileName)
      pl.plot(plotFig, filename = plotFileName + '.html', show_link = False, auto_open = False)



if args.verbose:
  print('Done.')

