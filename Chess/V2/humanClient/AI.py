# -*- coding: iso-8859-1 -*-
#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

import re

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  def init(self):
    pass

  def end(self):
    pass
  
  def displayBoard(self):
    print '-' * 26
    l = '8'
    for i in reversed(self.board):
      print '|' + '|'.join(i) + '| ' + l
      print '-' * 26
      l = chr(ord(l)-1)
    print ' A  B  C  D  E  F  G  H'
    
  def move(self):
    while True:
      m = raw_input('Enter move: ') + 'Q'
      if not re.match('[A-H][1-8]-[A-H][1-8]', m):
        print "Invalid format."
        continue
      rank = int(m[1])
      file = ord(m[0]) - ord('A') + 1
      piece = None
      for i in self.pieces:
        if i.getRank() == rank and i.getFile() == file:
          piece = i
          break
      if not piece:
        print 'No such piece.'
        continue
      
      rank = int(m[4])
      file = ord(m[3]) - ord('A') + 1
      type = ord(m[5])
      piece.move(file, rank, type)
      break

  def run(self):
    self.board = [ ['  '] * 8 for i in xrange(8) ]
    for i in self.pieces:
      self.board[i.getRank()-1][i.getFile()-1] = chr(i.getType()) + ('*' if i.getOwner() else ' ')
    self.displayBoard()
    
    self.move()
    
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
