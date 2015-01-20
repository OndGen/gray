#!/usr/bin/python


#
# triangles-spiral.py
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
      im.putpixel((rc[0], rc[1]), (block[rc[0], rc[1]]) * step)
  im.save(fileprefix+".png")
  del im


def generateTriangle(N, k, maxBlock, maxIteration):
  Zn = range(0, N);

  x0 = int(maxBlock / 2)
  y0 = int(maxBlock / 2)
  currentPosition = [ x0, y0 ]
  block = {}
  prev = None
  dx = 0
  dy = 0


  overallcount = 0
  tricount = 0
  dz = [ (-1, 1, 0), # downleft
       (0, -1, 0),   # down
       (1, 0, 0)]   # right 

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
    ZnIters += 1
    midx = 0


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
      movcount += 1
      if block[currentPosition[0], currentPosition[1]] == N-1:
        tricount += 1
        if tricount == k:
          return (block, ZnIters, overallcount) 
        midx = 0
      currentPosition[0] += d[0]
      currentPosition[1] += d[1]
      block[currentPosition[0], currentPosition[1]] = Zn[midx]
      midx += 1
      if midx == N:
        ZnIters += 1
        midx = 0

    if maxIteration < ZnIters:
      print "FAILED TO GENERATE A SPIRAL FOR N=%d, k=%d" % (N,k)
      return (None, ZnIters, overallcount)

  return (block, ZnIters, overallcount)

def main():

  for N in range(2,40):
    for k in range(1, 30):

# Need to think maxBlock, maxIteration through more
# just making this large since I dont know the generation formula
# then will cut the size down on image generation
#
      maxBlock = 5*k*N
      maxIteration = k*N*N*N*k

      (block, iterates, tris) = generateTriangle(N, k, maxBlock, maxIteration) 
      if block == None:
        print "Failed to generate Tri(N=%d, k=%d)" % (N,k)
        continue
 
      print "N=%d k=%d tris: %d iterations: %d" % (N, k, tris, iterates)

#      generateImages(block, maxBlock, N, 'tri-sp-N%d-k%d'%(N,k))

# We allocated more room than needed, so let's chop it down for image creation
# by just mapping translation to smaller block.

      keyset = block.keys()
      maxxy = map(max, zip(*keyset))
      maxy = maxxy[1]
      minxy = map(min, zip(*keyset))
      minx = minxy[0]
      miny = minxy[1]
      translated_block = {}
      for ks in keyset:
        translated_block[ks[0]-minx, ks[1]-miny] = block[ks[0], ks[1]]
      print "%d %d maxx=%d iters=%d" % (N, k, maxxy[0], iterates)
      generateImages(translated_block, maxy-miny+1, N, 'tri-sp-N%d-k%d'%(N,k))


if __name__ == '__main__':
  main()
