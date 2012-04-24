#!/usr/bin/env python

def number_spiral(h, w):
   # total number of elements in array
   n = w * h

   # start at top left (row 0 column 0)
   row, column = 0,0

   # first move is on the same row, to the right
   d_row, d_column = 0, 1

   # fill 2d array with dummy values we'll overwrite later
   arr = [[None ]* w for z in range(h)]

   for i in xrange(1,n+1):
      arr[row][column] = i

      # next row and column
      nrow, ncolumn = row + d_row, column + d_column

      if 0 <= nrow < h and 0 <= ncolumn < w and arr[nrow][ncolumn] == None:
         # no out of bounds accesses or overwriting already-placed elements.
         row, column = nrow, ncolumn
      else:
         # change direction
         d_row , d_column = d_column, -d_row
         row, column = row + d_row, column + d_column

   # print it out!
   for a in range(h):
      for b in range(w):
         print "%2i" % arr[a][b],
      print

def s(eq, var='x'):
    r = eval(eq.replace('=', '-(') + ')', {var:1j})
    return -r.real / r.imag

if __name__ == '__main__':
   number_spiral(5, 5)
