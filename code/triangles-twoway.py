#!/usr/bin/python

import sys
from PIL import Image
#import gmpy
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
  modNset = range(0, N);


  currentPosition = [ 0, maxBlock ]
  block = {}
  prev = None
  dx = 0
  dy = 0
 
  tricount = 0
  for jj in range(0, maxIteration+5):
    for mn in modNset:


      prev = currentPosition
      block[prev[0], prev[1]] = mn

      if prev[0] == 0 and prev[1] == maxBlock:  # At start
        currentPosition[0] += 1 
        currentPosition[1] += 0 
        dx = -1
        dy = -1
        continue

# we are moving up-left
      if dx == -1 and dy == -1:
        if prev[0] == 0:
#          print "You have reached x-min with mn=%d"%(mn)
          if mn == (N-1):
            tricount += 1
            if tricount == k:
              return (block, jj+1)
          currentPosition[1] += -1
          dx = dy = 1
        else:
          currentPosition[0] += dx
          currentPosition[1] += dy
      elif dx == 1 and dy == 1:
        if prev[1] == maxBlock:
#          print "You have reached y-max with mn=%d" % (mn)
          if mn == (N-1):
            tricount += 1
            if tricount == k:
              return (block, jj+1)
              return block
          #currentPosition[1] += -1
          currentPosition[0] += 1
          dx = dy = -1
        else:
          currentPosition[0] += dx
          currentPosition[1] += dy
  return (None, 0)

def main():

  for N in range(2, 20):
    for k in range(1, 30):

# Need to think maxBlock, maxIteration through more
# just making this large since I dont know the generation formula
# then will cut the size down on image generation
#
      maxBlock = k*k*k*N*N
      maxIteration = k*k*k*N*N*N

      (block, iterates) = generateTriangle(N, k, maxBlock, maxIteration) 
      if block == None:
        print "Failed to generate Tri(N=%d, k=%d)" % (N,k)
        continue


# We allocated more room than needed, so let's chop it down for image creation
# by just mapping translation to smaller block.
      keyset = block.keys()
      maxxy = map(max, zip(*keyset))
      maxy = maxxy[1]
      minxy = map(min, zip(*keyset))
      miny = minxy[1]
      translated_block = {}
      for ks in keyset:
        translated_block[ks[0], ks[1]-miny] = block[ks[0], ks[1]]
      print "%d %d maxx=%d iters=%d" % (N, k, maxxy[0], iterates)
      generateImages(translated_block, maxy-miny+1, N, 'Tri-two-N%d-k%d'%(N,k))


if __name__ == '__main__':
  main()
