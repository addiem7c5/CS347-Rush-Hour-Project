#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

class Node:
   piece = None
   move = None
   
class AI(BaseAI):
  """The class implementing gameplay logic."""
  board = []
  lower = 0
  upper = 1
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"
  def buildBoard(self):
    self.board = [['.','.','.','.','.','.','.','.'],
                  ['.','.','.','.','.','.','.','.'],
                  ['.','.','.','.','.','.','.','.'],
                  ['.','.','.','.','.','.','.','.'],
                  ['.','.','.','.','.','.','.','.'],
                  ['.','.','.','.','.','.','.','.'],
                  ['.','.','.','.','.','.','.','.'],
                  ['.','.','.','.','.','.','.','.']]
    for p in self.pieces:
      if p.getOwner() == 0:
        self.board[p.getRank()-1][p.getFile()-1] = str.lower(chr(p.getType()))
      else:
        self.board[p.getRank()-1][p.getFile()-1] = chr(p.getType())

  def printBoard(self):
    str = ""
    for a in self.board:
      for b in a:
        str+=b
      str+='\n'
    print str

  def kingMoves(self, piece):
    f = piece.getFile() - 1
    r = piece.getRank() - 1
    
    moves = []
    if f + 1 <= 7:
      if self.board[r][f+1].islower() ^ piece.getOwner():
        moves.append([piece, r, f+1])
      if r - 1 >= 0 and self.board[r-1][f+1].islower() ^ piece.getOwner():
        moves.append([piece, r-1, f+1])
      if r + 1 <= 7 and self.board[r+1][f+1].islower() ^ piece.getOwner():
        moves.append([piece, r+1, f+1])

    elif f - 1 >= 0:
      if self.board[r][f-1].islower() ^ piece.getOwner():
        moves.append([piece, r, f-1])
      if r - 1 >= 0 and self.board[r-1][f-1].islower() ^ piece.getOwner():
        moves.append([piece, r-1, f-1])
      if r + 1 <= 7 and self.board[r+1][f-1].islower() ^ piece.getOwner():
        moves.append([piece, r+1, f-1])
    return moves

  def queenMoves(self, piece):
    f = piece.getFile() - 1
    r = piece.getRank() - 1
    moves = []
    for ypos in range(f+1, 8):
      if self.board[r][ypos] == '.':
        moves.append([piece, r, ypos])
      elif self.board[r][ypos].islower() ^ piece.getOwner():
        moves.append([piece, r, ypos])
        break
    for yneg in range(f-1, 0):
      if self.board[r][yneg] == '.':
        moves.append([piece, r, yneg])
      elif self.board[r][yneg].islower() ^ piece.getOwner():
        moves.append([piece, r, yneg])
        break

    for xpos in range(r+1, 8):
      if self.board[xpos][f] == '.':
        moves.append([piece, xpos, f])
      elif self.board[xpos][f].islower() ^ piece.getOwner():
        moves.append([piece, xpos, f])
        break

    for xneg in range(r-1, 0):
      if self.board[f][xneg] == '.':
        moves.append([piece, xneg, f])
      elif self.board[xneg][f].islower() ^ piece.getOwner():
        moves.append([piece, xneg, f])
        break
       
    return moves

  def bishopMoves(self, file, rank, owner):
    return []
  def knightMoves(self, file, rank, owner):
    return []
  def rookMoves(self, file, rank, owner):
    return []
  def pawnMoves(self, file, rank, owner):
    
    return []
  def kingInCheck(self, file, rank):
    pass

  def whatCanMove(self):
    moves = []
    for p in self.pieces:
      if p.getOwner() == self.playerID():
        if chr(p.getType()) == 'K':
          moves += self.kingMoves(p)
        elif chr(p.getType()) == 'Q':
          moves += self.queenMoves(p)
        elif chr(p.getType()) == 'B':
          moves += self.bishopMoves(p.getFile(), p.getRank(), p.getOwner())
        elif chr(p.getType()) == 'N':
          moves += self.knightMoves(p.getFile(), p.getRank(), p.getOwner())
        elif chr(p.getType()) == 'R':
          moves += self.rookMoves(p.getFile(), p.getRank(), p.getOwner())
        elif chr(p.getType()) == 'P':
          moves += self.pawnMoves(p.getFile(), p.getRank(), p.getOwner())
    return moves
        
  def init(self):
    pass

  def end(self):
    pass

  def run(self):
    self.buildBoard()
    self.printBoard()
    print self.playerID()
    for a in self.whatCanMove():
      print a[0].getRank(), a[0].getFile(), chr(a[0].getType()), a[1], a[2]
    
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
