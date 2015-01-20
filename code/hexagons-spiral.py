#!/usr/bin/python


#
# centered hexagons
#
# hexagons-spiral.py
#
#

import sys
from PIL import Image
from math import sqrt
import operator
from operator import itemgetter
from collections import defaultdict
import time

def generateImages(block, maxSquareSize, N, fileprefix):
  
  im = Image.new("L", (maxSquareSize, maxSquareSize))
  step = int(255/N) + 1
  for rc in block.keys():
#      im.putpixel((rc[0], rc[1]), 255)   # validator to make sure we miss no pixels
#      print "%d %d" % (rc[0], rc[1])
      im.putpixel((rc[0], rc[1]), (block[rc[0], rc[1]]) * step)
  im.save(fileprefix+".png")
  del im


def generateHexagon(N, k, maxBlock, maxIteration):
  Zn = range(0, N);

  x0 = int(maxBlock / 2)
  y0 = int(maxBlock / 2)
  currentPosition = [ x0, y0 ]
  block = {}
  prev = None
  dx = 0
  dy = 0

  overallcount = 0
  hexcount = 0
  dz = [ (0, 1, -1), # move down -1 times
       (-1, 1, 0),   # left-down
       (-1, 0, 0),   # left
       (0, -1, 0),   # up
       (1, -1, 0),   # up-right
       (1, 0, 0) ]   # right

  midx = 0
  # Number of times each dz is applied
  movcount = 1
  dzidx = 0
  ZnIters = 0 

  block[currentPosition[0], currentPosition[1]] = Zn[midx]
  midx += 1
  currentPosition[0] += 1 
  block[currentPosition[0], currentPosition[1]] = Zn[midx]
  midx += 1
  if midx == N:
    midx = 0
    ZnIters += 1

  while True:
    for d in dz:
      rmc = movcount + d[2]
      for move in range(0, rmc):
        currentPosition[0] += d[0]
        currentPosition[1] += d[1]
        block[currentPosition[0], currentPosition[1]] = Zn[midx]
        midx += 1
        if midx == N:
          ZnIters += 1
          midx = 0
#        print "midx=%d" % (midx)

    overallcount += 1
    if maxIteration < ZnIters:
      print "FAILED TO GENERATE A SPIRAL FOR N=%d, k=%d" % (N,k)
      return (None, ZnIters, overallcount)
    movcount += 1
    if block[currentPosition[0], currentPosition[1]] == N-1:
      hexcount += 1
      if hexcount == k:
        break
      midx = 0
    currentPosition[0] += 1 
    currentPosition[1] += 0
    block[currentPosition[0], currentPosition[1]] = Zn[midx]
    midx += 1
    if midx == N:
      ZnIters += 1
      midx = 0
#    print "midx=%d" % (midx)

  return (block, ZnIters, overallcount)

def main():

  for N in [7, 13, 19, 31, 37, 43, 49, 61, 67, 73, 79, 91, 97]:


    for k in range(1, 40):

# Need to think maxBlock, maxIteration through more
# just making this large since I dont know the generation formula
# then will cut the size down on image generation
#
      maxBlock = 5*k*N
      maxIteration = k*N*N*k

      (block, iterates, hexes) = generateHexagon(N, k, maxBlock, maxIteration) 
      if block == None:
        print "Failed to generate Hex(N=%d, k=%d) skipping this N entirely" % (N,k)
        break

      print "N=%d k=%d hexes: %d iterations: %d" % (N, k, hexes, iterates)
#      generateImages(block, maxBlock, N, 'hex-sp-N%d-k%d'%(N,k))

# We allocated more room than needed, so let's chop it down for image creation
# by just mapping translation to smaller block.

      keyset = block.keys()
      maxxy = map(max, zip(*keyset))
      maxx = maxxy[0]
      maxy = maxxy[1]
      minxy = map(min, zip(*keyset))
      minx = minxy[0]
      miny = minxy[1]
      translated_block = {}
      for ks in keyset:
        translated_block[ks[0]-minx, ks[1]-miny] = block[ks[0], ks[1]]
#      print "%d %d xmin=%d xmax=%d ymin=%d ymax=%d iters=%d" % (N, k, minx, maxx, miny, maxy, iterates)
      generateImages(translated_block, maxy-miny+1, N, 'hex-sp-N%d-k%d'%(N,k))


if __name__ == '__main__':
  main()
