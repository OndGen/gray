#!/usr/bin/python

#
# this is for the hexagonal numbers
#
import sys
from PIL import Image
#import gmpy
from math import sqrt
import operator
from operator import itemgetter
from collections import defaultdict
import time

def generateImages(block, maxSquareSize, N, fileprefix):
  
  ks = block.keys()
  im = Image.new("L", (maxSquareSize+1, maxSquareSize+1))
  step = int(255/N) + 1
  for rc in block.keys():
#      im.putpixel((rc[0], rc[1]), 255) # validator
      im.putpixel((rc[0], rc[1]), (block[rc[0], rc[1]]) * step)
  im.save(fileprefix+".png")
  del im


def generateHexagon(N, k, maxBlock, maxIteration):
  modNset = range(0, N);



  currentPosition = [ 0, maxBlock ]
  block = {}

  # up, up-right, right, down, down-left
  directions = [ (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1) ]
 
  dxy = directions[0] 
  hexcount = 0
  move_count_lim = 1
  move_count_min = 0
  move_count = 0
  dir_ind = 0
  maxx = 0
  maxy = maxBlock

  for jj in range(0, maxIteration+5):
    for mn in modNset:


      prev = currentPosition
      block[prev[0], prev[1]] = mn

# We have reached
      if prev[0] == maxx+1 and prev[1] == maxBlock:
        maxx += 1
        if mn == (N-1):
          hexcount += 1
          if hexcount == k:
            return (block, jj+1)
        dir_ind = 0
        move_count_lim += 1
        move_count_min += 1
        move_count = move_count_min
        currentPosition[0] = 0
        maxy -= 1
        currentPosition[1] = maxy
      else:
        currentPosition[0] += directions[dir_ind][0]
        currentPosition[1] += directions[dir_ind][1]
        move_count += 1
        if move_count == move_count_lim:
          dir_ind += 1
          move_count = 0
  return (None, 0)


def main():

  for N in range(20, 30):
    for k in range(1, 30):
      maxBlock = N*N*N*k
      maxIteration = maxBlock*N*N
      (block, iters) = generateHexagon(N, k, maxBlock, maxIteration) 
      if block == None:
        print "Unable to create Hex(%d, %d)" % (N, k)
        continue
      keyset = block.keys()
      maxxy = map(max, zip(*keyset))
      maxy = maxxy[1]
      minxy = map(min, zip(*keyset))
      miny = minxy[1]
      translated_block = {}
      for ks in keyset:
        translated_block[ks[0], ks[1]-miny] = block[ks[0], ks[1]]
      print "%d %d maxx=%d iters=%d" % (N, k, maxxy[0], iters)
      generateImages(translated_block, maxy-miny, N, 'Hex-one-N%d-k%d'%(N,k))    


if __name__ == '__main__':
  main()
