#!/usr/bin/python

#
# Not the most pretty code. :-/ nor efficient... but so it goes.
#
# After you run and generate, run:
#	convert <ond.png> -rotate 180 <out.png>
#
# As this code is doing things a bit oddly :<D
#

import sys
from PIL import Image
from math import sqrt
import operator
from collections import defaultdict
import time


gend = {}

def generateImages(block, maxSquareSize, N, fileprefix):
  im = Image.new("L", (maxSquareSize, maxSquareSize))
  step = int(255/N) + 1
  for rc in block.keys():
      im.putpixel((rc[0], rc[1]-1), (block[rc[0], rc[1]]+1) * step)
#      im.putpixel((rc[0], rc[1]-1), 255) # validator.. make all white thepixels you step on
  im.save(fileprefix+".png")
  del im


def generateSquare(N, k):
  modNSet = range(0, N)
  maxsquares = getMaximalSquares(N)
  msk = maxsquares.keys()
  denom = 1
  for zz in msk:
    denom *= sqrt(maxsquares[zz])

  maxSquareSize = int((k*N)/denom)
  maxIterationCount = int((k*k*N)/(denom*denom))
  print maxIterationCount
  currentPosition = [ int(maxSquareSize / 2), int(maxSquareSize / 2) ]
  dx = 1
  dy = 0
  squareCount = 0
  block = {}
  prev = currentPosition
  for jj in range(0, maxIterationCount+5):
    for mn in modNSet:
      prev = currentPosition
      if currentPosition[1] == 0:
        print "y=0, dx=%d, dy=%d" % ( dx, dy)
      # We are moving right
      if dx == 1:
        testEntry = ( currentPosition[0], currentPosition[1] + 1 )
        if testEntry not in block:
          block[testEntry[0], testEntry[1]] = mn
          dx = 0
          dy = 1
          currentPosition = [testEntry[0], testEntry[1]]
          continue
        block[currentPosition[0] + 1, currentPosition[1]] = mn
        currentPosition[0] += 1
        continue
      # We are moving left
      elif dx == -1: 
        testEntry = ( currentPosition[0], currentPosition[1] - 1 )
        if testEntry not in block:
          block[testEntry[0], testEntry[1]] = mn
          dx = 0
          dy = -1
          currentPosition = [testEntry[0], testEntry[1]]
          continue
        block[currentPosition[0] - 1, currentPosition[1]] = mn
        currentPosition[0] -= 1
        continue
      # We are moving up
      elif dy == 1:
        testEntry = ( currentPosition[0] - 1, currentPosition[1] )
        if testEntry not in block:
          block[testEntry[0], testEntry[1]] = mn
          dx = -1
          dy = 0
          currentPosition = [testEntry[0], testEntry[1]]
          continue
        block[currentPosition[0], currentPosition[1] + 1] = mn
        currentPosition[1] += 1
        continue
      # We are moving down
      elif dy == -1:
        testEntry = ( currentPosition[0] + 1, currentPosition[1] )
        if testEntry not in block:
          block[testEntry[0], testEntry[1]] = mn
          dx = 1
          dy = 0
          currentPosition = [testEntry[0], testEntry[1]]
          continue
        block[currentPosition[0], currentPosition[1] - 1] = mn
        currentPosition[1] -= 1
        continue
      else:
        print "Bad state in spiraling! dx=%d dy=%d\n" % (dx, dy)
        sys.exit(10)

      if currentPosition[0] < 0:
        print "Bad position"
#        print block
      elif currentPosition[1] < 0:
        print "Bad position"
#        print block
    
    # Are we a square at this point?
    coords = block.keys()
    if is_square(len(coords)):
      root = int(sqrt(len(coords)))
      squareCount += 1
      minx = min(coords, key=operator.itemgetter(0))
      maxx = max(coords, key=operator.itemgetter(0))
      miny = min(coords, key=operator.itemgetter(1))
      maxy = max(coords, key=operator.itemgetter(1))
      if (maxx[0]-minx[0]) != (maxy[1]-miny[1]):
        print "min/max dumb test failed!"
 
      isTop = True
      if prev[1] == maxy[1]:
        isTop = True
      else:
        isTop = False

      if squareCount == k:
        generateImages(block, maxSquareSize, N, "Ond-N%d-k%d" % (N, squareCount))
        gend[N,k] = (root, jj+1)      
        del block
        return isTop

def primes(n):
  primfac = []
  d = 2
  while d*d <= n:
    while (n % d) == 0:
      primfac.append(d)  # supposing you want multiple factors repeated
      n /= d
    d += 1
  if n > 1:
    primfac.append(n)
  return primfac

def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True

def getMaximalSquares(N):
  factors = primes(N)

  part = defaultdict(list)
  for f in factors:
    part[f].append(f)
  maxsquares = {}
  maxsquares[1] = 1
  pk = part.keys() 
  for k in pk:
    pcnt = len(part[k])
    if pcnt == 1:
      continue
    maxsq = 1
    for j in part[k]:
      maxsq *= j
    while pcnt > 2:
      if is_square(maxsq) == False:
        maxsq /= k
        pcnt -= 1
        continue
      break
    maxsquares[k] = maxsq
  return maxsquares

def testSpirals(args):
  isTop = {} 
  (N_MIN, N_MAX, k_MIN, k_MAX) = args
  for N in range(N_MIN, N_MAX+1):
    print N
    sys.stdout.flush()
    for k in range(k_MIN, k_MAX+1):
      T = generateSquare(N, k)
      isTop[N,k] = T

  for N in range(N_MIN, N_MAX+1):

# bit of a hck
    maxsquares = getMaximalSquares(N)
    for k in range(k_MIN,k_MAX+1):
      type = ""
      msk = maxsquares.keys()
      ldenom = 1
      idenom = 1
      for zz in msk:
        ldenom *= sqrt(maxsquares[zz])
        idenom *= maxsquares[zz]

#      # (kN/ldenom, kkN/idenom)
#      if gend[N,k][0] == (k*N)/ldenom and gend[N,k][1] == (k*k*N)/idenom:
      print "[%d, %d]: (%d, %d) %s" % (N, k, gend[N,k][0], gend[N,k][1], str(primes(N)))
#      else:
#        print "[%d, %d]: (%d, %d) ~ FAIL ~ Top=%s" % (N, k, gend[N,k][0], gend[N,k][1], str(isTop[N,k]))
      
def main():

  inputs = [ (2, 50, 1, 5),
             (51, 100, 1, 5),
             (101, 150, 1, 5),
             (151, 200, 1, 5),
             (201, 250, 1, 5),
             (251, 300, 1, 5),
             (301, 350, 1, 5),
             (351, 400, 1, 5),
             (401, 450, 1, 5),
             (451, 500, 1, 5) ]

  inputs = [ (3, 9, 4, 8) ]
  for ii in inputs:
    t0 = time.time()
    testSpirals(ii)
    t1 = time.time()
    print "%s time: %f seconds" % (str(ii), t1-t0)

          
if __name__ == "__main__":
  main()
