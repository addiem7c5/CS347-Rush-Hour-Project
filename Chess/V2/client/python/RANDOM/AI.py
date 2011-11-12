#-*-python-*-
#########################
#File: AI.py            #
#Author: Addie Martin   #
#########################
from BaseAI import BaseAI
from GameObject import *
import random
import sys
import operator

#made this global cause I had to, it's silly and lame, but god damnit it works
enpassants = []

###################################################################
#Function: kingInCheck()                                          #
#Arguments: the rank that a piece is moving from, the file a piece#
#           is moving from, the rank that piece is moving to, and #
#           the file that piece is moving to. Also a flag to det- #
#           ermine if this is an enpassant move, so we know to    #
#           change the current board in two spaces.               #
#Returns: True if the king is in check, False otherwise           #
#Description: This checks if the move specified by the arguments  #
#             causes the king to be in check by any opponents     #
#             piece on the board. I copy the current board state  #
#             and change it to look like what it would look like  #
#             after the move specified and see if the king is in  #
#             check.                                              #
###################################################################
def kingInCheck(board, playerID, fromrank, fromfile, torank, tofile, kingrank, kingfile, enpassant = False):
  state = []
  temp = []
  for a in board:
    for b in a:
      temp.append(b)
    state.append(temp)
    temp = []
  kr = 0
  kf = 0


  state[torank][tofile] = state[fromrank][fromfile]
  state[fromrank][fromfile] = '.'
  #change the board in 2 spaces for enpassant
  if enpassant == True:
    if fromrank == 3:
      state[torank+1][tofile] = '.'
    elif fromrank == 4:
      state[torank-1][tofile] = '.'

  if fromrank == kingrank and fromfile == kingfile:
    kr = torank
    kf = tofile
  else:
    kr = kingrank
    kf = kingfile
  
  dl = 0
  dr = 0
  ul = 0
  ur = 0

  #CHECKING FOR CHECK BY PAWN, KING (if i==1), BISHOP OR QUEEN TO THE DIAGONALS
  for i in range(1, 8):
    if dr == 0 and ((i == 1 and playerID == 1 and kf+i <= 7 and kr+i <= 7 and state[kr+i][kf+i].islower() != state[kr][kf].islower() and state[kr+i][kf+i].upper() == "P") or \
                    (i == 1 and kf+i <= 7 and kr+i <= 7 and state[kr+i][kf+i].islower() != state[kr][kf].islower() and state[kr+i][kf+i].upper() == "K") or \
                    (i >= 1 and kf+i <= 7 and kr+i <= 7 and state[kr+i][kf+i].islower() != state[kr][kf].islower() and state[kr+i][kf+i].upper() in "QB")):
      return True
    elif dr == 0 and (kr+i <= 7 and kf+i <= 7 and state[kr+i][kf+i] != '.') and ((kf+i <= 7 and kr+i <= 7 and (state[kr+i][kf+i].islower() == state[kr][kf].islower() or (i == 1 and state[kr+i][kf+i].upper() in "RN") or (i > 1 and state[kr+i][kf+i].upper() in "RNPK")) or kf+i > 7 or kr + i > 7)):
      dr = 1
    if dl == 0 and ((i == 1 and playerID == 1 and kf-i >= 0 and kr+i <= 7 and state[kr+i][kf-i].islower() != state[kr][kf].islower() and state[kr+i][kf-i].upper() in "P") or \
                    (i == 1 and kf-i >= 0 and kr+i <= 7 and state[kr+i][kf-i].islower() != state[kr][kf].islower() and state[kr+i][kf-i].upper() == "K") or \
                    (i >= 1 and kf-i >= 0 and kr+i <= 7 and state[kr+i][kf-i].islower() != state[kr][kf].islower() and state[kr+i][kf-i].upper() in "QB")):
      return True
    elif dr == 0 and (kr+i <= 7 and kf-i >= 0 and state[kr+i][kf-i] != '.') and ((kf-i >= 0 and kr+i <= 7 and (state[kr+i][kf-i].islower() == state[kr][kf].islower() or (i == 1 and state[kr+i][kf-i].upper() in "RN") or (i > 1 and state[kr+i][kf-i].upper() in "RNPK")) or kf-i > 7 or kr + i > 7)):
      dl = 1
    
    if ul == 0 and ((i == 1 and playerID == 0 and kf-i >= 0 and kr-i >= 0 and state[kr-i][kf-i].islower() != state[kr][kf].islower() and state[kr-i][kf-i].upper() in "P") or \
                    (i == 1 and kf-i >= 0 and kr-i >= 0 and state[kr-i][kf-i].islower() != state[kr][kf].islower() and state[kr-i][kf-i].upper() == "K") or \
                    (i >= 1 and kf-i >= 0 and kr-i >= 0 and state[kr-i][kf-i].islower() != state[kr][kf].islower() and state[kr-i][kf-i].upper() in "QB")):
      return True
    elif ul == 0 and (kr-i >= 0 and kf-1 >= 0 and state[kr-i][kf-i] != '.') and ((kf-i >= 0 and kr-i >= 0 and (state[kr-i][kf-i].islower() == state[kr][kf].islower() or (i == 1 and state[kr-i][kf-i].upper() in "RN") or (i > 1 and state[kr-i][kf-i].upper() in "RNPK")) or kf-i > 7 or kr-i > 7)):
      ul = 1   
    
    if ur == 0 and ((i == 1 and playerID == 0 and kf+i <= 7 and kr-i >= 0 and state[kr-i][kf+i].islower() != state[kr][kf].islower() and state[kr-i][kf+i].upper() == "P") or \
                    (i == 1 and kf+i <= 7 and kr-i >= 0 and state[kr-i][kf+i].islower() != state[kr][kf].islower() and state[kr-i][kf+i].upper() == "K") or \
                    (i >= 1 and kf+i <= 7 and kr-i >= 0 and state[kr-i][kf+i].islower() != state[kr][kf].islower() and state[kr-i][kf+i].upper() in "QB")):
      return True
    elif ur == 0 and (kr-i >= 0 and kf+i <= 7 and state[kr-i][kf+i] != '.') and ((kf+i <= 7 and kr-i >= 0 and (state[kr-i][kf+i].islower() == state[kr][kf].islower() or (i == 1 and state[kr-i][kf+i].upper() in "RN") or (i > 1 and state[kr-i][kf+i].upper() in "RNPK")) or kf+i > 7 or kr-i > 7)):
      ur = 1
    if dl == 1 and dr == 1 and ul == 1 and ur == 1:
      break

  #CHECKING TO SEE IF ITS IN CHECK BY ROOK, QUEEN (up/down, left/right) or KING(up/down, left/right)
  for i in range(kf+1, 8):
    if state[kr][i] != '.' and state[kr][i].islower() != state[kr][kf].islower() and \
        ((state[kr][i].upper() == 'K' and i == kf+1) or state[kr][i].upper() in 'QR'):
      return True
    elif state[kr][i] != '.' and (state[kr][i].islower() == state[kr][kf].islower() or state[kr][i] not in "KRQ.krq"):
      break
  for i in range(kf-1, -1, -1):
    if state[kr][i] != '.' and state[kr][i].islower() != state[kr][kf].islower() and \
        ((state[kr][i].upper() == 'K' and i == kf-1) or state[kr][i].upper() in 'QR'):
      return True
    elif state[kr][i] != '.' and (state[kr][i].islower() == state[kr][kf].islower() or state[kr][i] not in "KRQ.krq"):
      break
  for i in range(kr+1, 8):
    if state[i][kf] != '.' and state[i][kf].islower() != state[kr][kf].islower() and \
        ((state[i][kf].upper() == 'K' and i == kr+1) or state[i][kf].upper() in 'QR'):
      return True
    elif state[i][kf] != '.' and (state[i][kf].islower() == state[kr][kf].islower() or state[i][kf] not in "KRQ.krq"):
      break
  for i in range(kr-1, -1, -1):
    if state[i][kf] != '.' and state[i][kf].islower() != state[kr][kf].islower() and \
        ((state[i][kf].upper() == 'K' and i == kr-1) or state[i][kf].upper() in 'QR'):
      return True
    elif state[i][kf] != '.' and (state[i][kf].islower() == state[kr][kf].islower() or state[i][kf].upper() not in "KRQ.krq"):
      break

  #CHECKING FOR CHECK BY KNIGHT
  
  if kr - 2 >= 0:
    if kf - 1 >= 0 and state[kr-2][kf-1].upper() == "N" and state[kr-2][kf-1].islower() != state[kr][kf].islower():
      return True
    if kf + 1 <= 7 and state[kr-2][kf+1].upper() == "N" and state[kr-2][kf+1].islower() != state[kr][kf].islower():
      return True
  if kr + 2 <= 7:
    if kf - 1 >= 0 and state[kr+2][kf-1].upper() == "N" and state[kr+2][kf-1].islower() != state[kr][kf].islower():
      return True
    if kf + 1 <= 7 and state[kr+2][kf+1].upper() == "N" and state[kr+2][kf+1].islower() != state[kr][kf].islower():
      return True
  
  if kf - 2 >= 0:
    if kr - 1 >= 0 and state[kr-1][kf-2].upper() == "N" and state[kr-1][kf-2].islower() != state[kr][kf].islower():
      return True
    if kr + 1 <= 7 and state[kr+1][kf-2].upper() == "N" and state[kr+1][kf-2].islower() != state[kr][kf].islower():
      return True
  if kf + 2 <= 7:
    if kr - 1 >= 0 and state[kr-1][kf+2].upper() == "N" and state[kr-1][kf+2].islower() != state[kr][kf].islower():
      return True
    if kr + 1 <= 7 and state[kr+1][kf+2].upper() == "N" and state[kr+1][kf+2].islower() != state[kr][kf].islower():
      return True

  return False    


####################################################################
#Function: kingMoves()                                             #
#Returns: list of moves for king in the format                     # 
#         [piece, [to rank, to file]]                              #
#Description: Determines possible moves for a king. It checks the  #
#             diagonals for moves right next to it.                #
#             If it finds a . it can move there. If it finds the   #
#             opponents piece, it can move there. If it finds a    #
#             friendly piece it can not move there.                #
#             It also checks if this move will cause the it to     #
#             be in check.                                         #
####################################################################  
def kingMoves(board, playerID, pieces, piece, kr, kf):
  f = piece.getFile() - 1
  r = piece.getRank() * -1 + 8
  moves = []
  if f + 1 <= 7:
    if (board[r][f+1] == '.' or \
        board[r][f+1].islower() != board[r][f].islower()) and \
        not kingInCheck(board, piece.getOwner(), r, f, r, f+1, kr, kf):
      moves.append([piece, rankFileTransform(r, f+1)])
    if r + 1 <= 7 and (board[r+1][f+1] == '.' or \
        board[r+1][f+1].islower() != board[r][f].islower()) and \
        not kingInCheck(board, piece.getOwner(), r, f, r+1, f+1, kr, kf):
      moves.append([piece, rankFileTransform(r+1, f+1)])
    if r - 1 >= 0 and (board[r-1][f+1] == '.' or \
        board[r-1][f+1].islower() != board[r][f].islower()) and \
        not kingInCheck(board, piece.getOwner(), r, f, r-1, f+1, kr, kf):
      moves.append([piece, rankFileTransform(r-1, f+1)])
  if f - 1 >= 0:
    if (board[r][f-1] == '.' or \
        board[r][f-1].islower() != board[r][f].islower()) and \
        not kingInCheck(board, piece.getOwner(), r, f, r, f-1, kr, kf):
      moves.append([piece, rankFileTransform(r, f-1)])
    if r - 1 >= 0 and (board[r-1][f-1] == '.' or \
        board[r-1][f-1].islower() != board[r][f].islower()) and \
        not kingInCheck(board, piece.getOwner(), r, f, r-1, f-1, kr, kf):

      moves.append([piece, rankFileTransform(r-1, f-1)])
    if r + 1 <= 7 and (board[r+1][f-1] == '.' or \
        board[r+1][f-1].islower() != board[r][f].islower()) and \
        not kingInCheck(board, piece.getOwner(), r, f, r+1, f-1, kr, kf):
      moves.append([piece, rankFileTransform(r+1, f-1)])
  if r - 1 >= 0 and (board[r-1][f] == '.' or \
      board[r-1][f].islower() != board[r][f].islower()) and \
        not kingInCheck(board, piece.getOwner(), r, f, r-1, f, kr, kf):
    moves.append([piece, rankFileTransform(r-1, f)])
  if r + 1 <= 7 and (board[r+1][f] == '.' or \
      board[r+1][f].islower() != board[r][f].islower()) and \
        not kingInCheck(board, piece.getOwner(), r, f, r+1, f, kr, kf):
    moves.append([piece, rankFileTransform(r+1, f)])

  #CASTLING
  if piece.getHasMoved() == False and not kingInCheck(board, piece.getOwner(), r, f, r, f, kr, kf):
    for a in pieces:
      if a.getOwner() == playerID and chr(a.getType()) == 'R' and a.getHasMoved() == False:
        if a.getFile() - 1 == 0:
          if board[r][f-1] == '.' and not kingInCheck(board, piece.getOwner(), r, f, r, f-1, kr, kf):
            if board[r][f-2] == '.' and not kingInCheck(board, piece.getOwner(), r, f, r, f-2, kr, kf):
              if board[r][f-3] == '.':
                moves.append([piece, rankFileTransform(r, f-2)])
          if board[r][f+1] == '.' and not kingInCheck(board, piece.getOwner(), r, f, r, f+1, kr, kf):
            if board[r][f+2] == '.' and not kingInCheck(board, piece.getOwner(), r, f, r, f+2, kr, kf):
              moves.append([piece, rankFileTransform(r, f+2)])
        elif a.getFile() - 1 == 7:
          if board[r][f+1] == '.' and not kingInCheck(board, piece.getOwner(), r, f, r, f+1, kr, kf):
            if board[r][f+2] == '.' and not kingInCheck(board, piece.getOwner(), r, f, r, f+2, kr, kf):
              moves.append([piece, rankFileTransform(r, f+2)])
          if board[r][f-1] == '.' and not kingInCheck(board, piece.getOwner(), r, f, r, f-1, kr, kf):
            if board[r][f-2] == '.' and not kingInCheck(board, piece.getOwner(), r, f, r, f-2, kr, kf):
              if board[r][f-3] == '.':
                moves.append([piece, rankFileTransform(r, f-2)])
  return moves 

####################################################################
#Function: bishopMoves()                                           #
#Returns: list of moves for bishops in the format                  # 
#         [piece, [to rank, to file]]                              #
#Description: Determines possible moves for a bishop. It checks the#
#             diagonals for moves starting right next to it.       #
#             If it finds a . it can move there and keeps iterat-  #
#             ing. If it finds the opponents piece, it adds the    #
#             move and stops iterating. If it finds a friendly     #
#             piece it adds no move and stops iterating.           #
#             It also checks if this move will cause the king to   #
#             be in check.                                         #
####################################################################
def bishopMoves(board, piece, kr, kf):
  f = piece.getFile() - 1
  r = piece.getRank() * -1 + 8
  moves = []
  ul = 0
  ur = 0
  dl = 0
  dr = 0
  for i in range(1, 8):
    if f+i <= 7 and r+i <= 7 and dr == 0:
      if board[r+i][f+i] == '.' and \
          not kingInCheck(board, piece.getOwner(), r, f, r+i, f+i, kr, kf):
        moves.append([piece, rankFileTransform(r+i, f+i)])
      elif board[r+i][f+i].islower() != board[r][f].islower() and \
          not kingInCheck(board, piece.getOwner(), r, f, r+i, f+i, kr, kf):
        moves.append([piece, rankFileTransform(r+i, f+i)])
        dr = 1
      elif board[r+i][f+i] != '.' and board[r+i][f+i].islower() == board[r][f].islower():
        dr = 1
    if f-i >= 0 and r+i <= 7 and dl == 0:
      if board[r+i][f-i] == '.' and \
          not kingInCheck(board, piece.getOwner(), r, f, r+i, f-i, kr, kf):
        moves.append([piece, rankFileTransform(r+i, f-i)])
      elif board[r+i][f-i].islower() != board[r][f].islower() and \
          not kingInCheck(board, piece.getOwner(), r, f, r+i, f-i, kr, kf):
        moves.append([piece, rankFileTransform(r+i, f-i)])
        dl = 1
      elif board[r+i][f-i] != '.' and board[r+i][f-i].islower() == board[r][f].islower():
        dl = 1
    if f-i >= 0 and r-i >= 0 and ul == 0:
      if board[r-i][f-i] == '.' and \
          not kingInCheck(board, piece.getOwner(), r, f, r-i, f-i, kr, kf):
        moves.append([piece, rankFileTransform(r-i, f-i)])
      elif board[r-i][f-i].islower() != board[r][f].islower() and \
          not kingInCheck(board, piece.getOwner(), r, f, r-i, f-i, kr, kf):
        moves.append([piece, rankFileTransform(r-i, f-i)])
        ul = 1
      elif board[r-i][f-i] != '.' and board[r-i][f-i].islower() == board[r][f].islower():
        ul = 1   
    if f+i <= 7 and r-i >= 0 and ur == 0:
      if board[r-i][f+i] == '.' and \
          not kingInCheck(board, piece.getOwner(), r, f, r-i, f+i, kr, kf):
        moves.append([piece, rankFileTransform(r-i, f+i)])
      elif board[r-i][f+i].islower() != board[r][f].islower() and \
          not kingInCheck(board, piece.getOwner(), r, f, r-i, f+i, kr, kf):
        moves.append([piece, rankFileTransform(r-i, f+i)])
        ur = 1
      elif board[r-i][f+i] != '.' and board[r-i][f+i].islower() == board[r][f].islower():
        ur = 1
  return moves

####################################################################
#Function: knightMoves()                                           #
#Returns: list of moves for knights in the format                  # 
#         [piece, [to rank, to file]]                              #
#Description: Determines possible moves for a knight. It checks the#
#             possible spots for a knight to move. If it finds a . #
#             then it can move there. If it finds an opponents     #
#             piece then it can move there. If it finds a friendly #
#             piece it can not move there.                         #
#             It also checks if this move will cause the king to   #
#             be in check.                                         #
####################################################################
def knightMoves(board,  piece, kr, kf):
  f = piece.getFile() - 1
  r = piece.getRank() * -1 + 8
  moves = []
  
  if f - 2 >= 0:
    if r - 1 >= 0 and (board[r-1][f-2] == '.' or \
        board[r-1][f-2].islower() != board[r][f].islower()) and \
          not kingInCheck(board, piece.getOwner(), r, f, r-1, f-2, kr, kf):
      moves.append([piece, rankFileTransform(r-1, f-2)])
    if r + 1 <= 7 and (board[r+1][f-2] == '.' or \
        board[r+1][f-2].islower() != board[r][f].islower()) and \
          not kingInCheck(board, piece.getOwner(), r, f, r+1, f-2, kr, kf):
      moves.append([piece, rankFileTransform(r+1, f-2)])
  if f + 2 <= 7:
    if r - 1 >= 0 and (board[r-1][f+2] == '.' or \
        board[r-1][f+2].islower() != board[r][f].islower()) and \
          not kingInCheck(board, piece.getOwner(), r, f, r-1, f+2, kr, kf):
      moves.append([piece, rankFileTransform(r-1, f+2)])
    if r + 1 <= 7 and (board[r+1][f+2] == '.' or \
        board[r+1][f+2].islower() != board[r][f].islower()) and \
          not kingInCheck(board, piece.getOwner(), r, f, r+1, f+2, kr, kf):
      moves.append([piece, rankFileTransform(r+1, f+2)])
  
  if r - 2 >= 0:
    if f - 1 >= 0 and (board[r-2][f-1] == '.' or \
        board[r-2][f-1].islower() != board[r][f].islower()) and \
          not kingInCheck(board, piece.getOwner(), r, f, r-2, f-1, kr, kf):
      moves.append([piece, rankFileTransform(r-2, f-1)])
    if f + 1 <= 7 and (board[r-2][f+1] == '.' or \
        board[r-2][f+1].islower() != board[r][f].islower()) and \
          not kingInCheck(board, piece.getOwner(), r, f, r-2, f+1, kr, kf):
      moves.append([piece, rankFileTransform(r-2, f+1)])
  if r + 2 <= 7:
    if f - 1 >= 0 and (board[r+2][f-1] == '.' or \
        board[r+2][f-1].islower() != board[r][f].islower()) and \
          not kingInCheck(board, piece.getOwner(), r, f, r+2, f-1, kr, kf):
      moves.append([piece, rankFileTransform(r+2, f-1)])
    if f + 1 <= 7 and (board[r+2][f+1] == '.' or \
        board[r+2][f+1].islower() != board[r][f].islower()) and \
          not kingInCheck(board, piece.getOwner(), r, f, r+2, f+1, kr, kf):
      moves.append([piece, rankFileTransform(r+2, f+1)])
  return moves

##################################################################
#Function: rookMoves()                                           #
#Returns: list of moves for rooks in the format                  # 
#         [piece, [to rank, to file]]                            #
#Description: Determines possible moves for a rook. It checks the#
#             row and column for moves starting right next to it.#
#             If it finds a . it can move there and keeps iterat-#
#             ing. If it finds the opponents piece, it adds the  #
#             move and stops iterating. If it finds a friendly   #
#             piece it adds no move and stops iterating.         #
#             It also checks if this move will cause the king to #
#             be in check.                                       #
##################################################################
def rookMoves(board, piece, kr, kf):
  f = piece.getFile() - 1
  r = piece.getRank() * -1 + 8
  moves = []
  
  for i in range(f+1, 8):
    if board[r][i] == '.' and \
        kingInCheck(board, piece.getOwner(), r, f, r, i, kr, kf) == False:
      moves.append([piece, rankFileTransform(r, i)])
    elif board[r][i] != '.' and board[r][i].islower() != board[r][f].islower() and \
        kingInCheck(board, piece.getOwner(), r, f, r, i, kr, kf) == False:
      moves.append([piece, rankFileTransform(r, i)])
      break
    elif board[r][i] != '.' and board[r][i].islower() == board[r][f].islower():
      break
  for i in range(f-1, -1, -1):
    if board[r][i] != '.' and board[r][i].islower() != board[r][f].islower() and \
        kingInCheck(board, piece.getOwner(), r, f, r, i, kr, kf) == False:
      moves.append([piece, rankFileTransform(r, i)])
      break
    elif board[r][i] == '.' and \
        kingInCheck(board, piece.getOwner(), r, f, r, i, kr, kf) == False:
      moves.append([piece, rankFileTransform(r, i)])
    elif board[r][i] != '.' and board[r][i].islower() == board[r][f].islower():
      break
  for i in range(r+1, 8):
    if board[i][f] != '.' and board[i][f].islower() != board[r][f].islower() and \
        kingInCheck(board, piece.getOwner(), r, f, i, f, kr, kf) == False:
      moves.append([piece, rankFileTransform(i, f)])
      break
    elif board[i][f] == '.' and \
        kingInCheck(board, piece.getOwner(), r, f, i, f, kr, kf) == False:
      moves.append([piece, rankFileTransform(i, f)])
    elif board[i][f] != '.' and board[i][f].islower() == board[r][f].islower():
      break
  for i in range(r-1, -1, -1):
    if board[i][f] != '.' and board[i][f].islower() != board[r][f].islower() and \
        kingInCheck(board, piece.getOwner(), r, f, i, f, kr, kf) == False:
      moves.append([piece, rankFileTransform(i, f)])
      break
    elif board[i][f] == '.' and \
        kingInCheck(board, piece.getOwner(), r, f, i, f, kr, kf) == False:
      moves.append([piece, rankFileTransform(i, f)])
    elif board[i][f] != '.' and board[i][f].islower() == board[r][f].islower():
      break
  return moves

##################################################################
#Function: pawnMoves()                                           #
#Returns: list of moves for pawns in the format                  # 
#         [piece, [to rank, to file]]                            #
#Description: Determines possible moves for a pawn. First it     #
#             finds which side the pawn is on, and sees if it can#
#             make a 1 space or 2 space move. It also sees if it #
#             can take a piece normally or by en passant.        #
#             It also checks if this move will cause the king to #
#             be in check.                                       #
##################################################################
def pawnMoves(board, piece, kr, kf):
  f = piece.getFile() - 1
  r = piece.getRank() * -1 + 8
  moves = []
  
  removes = []
  if piece.getOwner() == 0:
    if r - 1 >= 0 and board[r - 1][f] == '.' and \
        not kingInCheck(board, piece.getOwner(), r, f, r-1, f, kr, kf):
      if r - 1 == 0:
        moves.append([piece, rankFileTransform(r-1, f), 'Q'])
        moves.append([piece, rankFileTransform(r-1, f), 'N'])
      else:
        moves.append([piece, rankFileTransform(r-1, f)])
      if r == 6 and board[r - 2][f] == '.' and \
        not kingInCheck(board, piece.getOwner(), r, f, r-2, f, kr, kf):
        moves.append([piece, rankFileTransform(r-2, f)])
    if r - 1 >= 0 and f - 1 >= 0 and board[r - 1][f - 1] != '.' and \
                                      board[r - 1][f - 1].isupper() != board[r][f].isupper() and \
        not kingInCheck(board, piece.getOwner(), r, f, r-1, f-1, kr, kf):
      if r - 1 == 0:
        moves.append([piece, rankFileTransform(r-1, f-1), 'Q'])
        moves.append([piece, rankFileTransform(r-1, f-1), 'N'])
      else:
        moves.append([piece, rankFileTransform(r-1, f-1)])
    if r - 1 >= 0 and f + 1 <= 7 and board[r - 1][f + 1] != '.' and \
                                      board[r - 1][f + 1].isupper() != board[r][f].isupper() and \
        not kingInCheck(board, piece.getOwner(), r, f, r-1, f+1, kr, kf):
      if r - 1 == 0:
        moves.append([piece, rankFileTransform(r-1, f+1), 'Q'])
        moves.append([piece, rankFileTransform(r-1, f+1), 'N'])
      else:
        moves.append([piece, rankFileTransform(r-1, f+1)])
    #Lets do that enpassant checking!
    if r == 3:
      if f - 1 >= 0 and board[1][f-1] == 'P':
        enpassants.append([r, f, 1, f-1])
      if f + 1 <= 7 and board[1][f+1] == 'P':
        enpassants.append([r, f, 1, f+1])

    for a in enpassants:
      if r == a[0]:
        if board[a[2]][a[3]] == '.':
          if board[r][a[3]] == 'P' and \
            not kingInCheck(board, piece.getOwner(), r, f, r-1, a[3], kr, kf, True):
            moves.insert(0,[piece, rankFileTransform(r-1, a[3]), '', True])
            removes.append(a)
          else:
            removes.append(a)
    for a in removes:
      enpassants.remove(a)
    removes = [] 
  

  else:
    if r + 1 <= 7 and board[r + 1][f] == '.' and \
        not kingInCheck(board, piece.getOwner(), r, f, r+1, f, kr, kf):
      if r + 1 == 7:
        moves.append([piece, rankFileTransform(r+1, f), 'Q'])
        moves.append([piece, rankFileTransform(r+1, f), 'N'])
      else:
        moves.append([piece, rankFileTransform(r+1, f)])
      if r == 1 and board[r+2][f] == '.' and \
        not kingInCheck(board, piece.getOwner(), r, f, r+2, f, kr, kf):
        moves.append([piece, rankFileTransform(r+2, f)])
    if r + 1 <= 7 and f + 1 <= 7 and board[r + 1][f + 1] != '.' and \
                                      board[r + 1][f + 1].islower() != board[r][f].islower() and \
                                      not kingInCheck(board, piece.getOwner(), r, f, r+1, f+1, kr, kf):
      if r + 1 == 7:
        moves.append([piece, rankFileTransform(r+1, f+1), 'Q'])
        moves.append([piece, rankFileTransform(r+1, f+1), 'N'])
      else:
        moves.append([piece, rankFileTransform(r+1, f+1)])
    if r + 1 <= 7 and f - 1 >= 0 and board[r + 1][f - 1] != '.' and \
                                      board[r + 1][f - 1].islower() != board[r][f].islower() and \
                                      not kingInCheck(board, piece.getOwner(), r, f, r+1, f-1, kr, kf):
      if r + 1 == 7:
        moves.append([piece, rankFileTransform(r+1, f-1), 'Q'])
        moves.append([piece, rankFileTransform(r+1, f-1), 'N'])
      else:
        moves.append([piece, rankFileTransform(r+1, f-1)])
    #Enpassant checking for the other team! Woot woot!
    if r == 4:
      if f - 1 >= 0 and board[6][f-1] == 'p':
        enpassants.append([r, f, 6, f-1])
      if f + 1 <= 7 and board[6][f+1] == 'p':
        enpassants.append([r, f, 6, f+1])
    for a in enpassants:
      if r == a[0]:
        if board[a[2]][a[3]] == '.':
          if board[r][a[3]] == 'p' and \
            not kingInCheck(board, piece.getOwner(), r, f, r+1, a[3], kr, kf, True):
            moves.insert(0,[piece, rankFileTransform(r+1, a[3]), '', True])
            removes.append(a)
          else:
            removes.append(a)
    for a in removes:
      enpassants.remove(a)
    removes = [] 

  return moves

##################################################################
#Function: queenMoves()                                          #
#Returns: list of moves for queens in the format                 # 
#         [piece, [to rank, to file]]                            #
#Description: Determines possible moves for a queen, by running  #
#             the find bishop moves and find rook moves on the   #
#             queen piece and adding them together.              #
##################################################################
def queenMoves(board, piece, kr, kf):
  return (bishopMoves(board, piece, kr, kf) + rookMoves(board, piece, kr, kf))

##################################################################
#Function: whatCanMove()                                         #
#Returns: list of moves in the format [piece, [to rank, to file]]#
#Description: Determines pieces that are owned by this player and#
#             sends them to their respective move finding        #
#             functions.                                         #
##################################################################
def whatCanMove(board, playerID, pieces, kr, kf):
  moves = []
  for p in pieces:
    if p.getOwner() == playerID:
      if chr(p.getType()) == 'K':
        moves += kingMoves(board, playerID, pieces, p, kr, kf)
      elif chr(p.getType()) == 'Q':
        moves += queenMoves(board, p, kr, kf)
      elif chr(p.getType()) == 'B':
        moves += bishopMoves(board, p, kr, kf)
      elif chr(p.getType()) == 'N':
        moves += knightMoves(board, p, kr, kf)
      elif chr(p.getType()) == 'R':
        moves += rookMoves(board, p, kr, kf)
      elif chr(p.getType()) == 'P':
        moves += pawnMoves(board, p, kr, kf)
  return moves

###################################################################
#Class: myPiece                                                   #
#Description: This gives me a handle on pieces that look like     #
#             pieces on the server, so I can change them. :)      #
##################################################################$
class myPiece:
  def __init__(self, piece):
    self.type = piece.getType()
    self.rank = piece.getRank()
    self.file = piece.getFile()
    self.playerID = piece.getOwner()
    self.hasMoved = piece.getHasMoved()
  def getType(self):
    return self.type
  def getRank(self):
    return self.rank
  def getFile(self):
    return self.file
  def getOwner(self):
    return self.playerID
  def getHasMoved(self):
    return self.getHasMoved

###################################################################
#Function: createChild()                                          #
#Returns: Newly Built Node                                        #
#Description: Copies the board state and applies a move to it.    #
#             and constructs a new node.                          #
#Arguments: current board state, pieces, move, whether it's black #
#           or white, minimax type, and the node depth.           #
##################################################################$
def createChild(board, pieces, move, blackwhite, mmtype, depth):
  newnode = Node()
  temp = []
  newnode.blackwhite = blackwhite
  newnode.mmtype = mmtype
  newnode.depth = depth
  newnode.movethatgotmehere = move
  kingrank = 0
  kingfile = 0      
  for a in board:
    for b in a:
      temp.append(b)
      if blackwhite == 0 and b == 'k':
        kingfile = a.index(b)
        kingrank = board.index(a)
      elif blackwhite == 1 and b == 'K':
        kingfile = a.index(b)
        kingrank = board.index(a)
    newnode.board.append(temp)
    temp = []
  fromrank = move[0].getRank() * -1 + 8
  fromfile = move[0].getFile() - 1
  torank = move[1][0] * -1 + 8
  tofile = move[1][1] - 1
  
  newnode.board[torank][tofile] = newnode.board[fromrank][fromfile]
  newnode.board[fromrank][fromfile] = '.'
  #change the board in 2 spaces for enpassant
  if len(move) == 4 and move[3] == True:
    if fromrank == 3:
      newnode.board[torank+1][tofile] = '.'
    elif fromrank == 4:
      newnode.board[torank-1][tofile] = '.'

  if fromrank == kingrank and fromfile == kingfile:
    newnode.kingrank = torank
    newnode.kingfile = tofile
  else:
    newnode.kingrank = kingrank
    newnode.kingfile = kingfile

  for a in pieces:
    if not (a.getFile() - 1 == tofile and a.getRank() * -1 + 8 == torank):
      if isinstance(a, Piece):
        temp = myPiece(a)
        newnode.pieces.append(temp)
      else:
        newnode.pieces.append(a)
      if a.getType() == move[0].getType() and a.getOwner() == move[0].getOwner() and \
         a.getRank() == move[0].getRank() and a.getFile() == move[0].getFile():
        newnode.pieces[-1].rank == move[1][0]
        newnode.pieces[-1].file == move[1][1]
  return newnode

###################################################################
#Class: Node                                                      #
#Description: Node to be used in the minimax algorithm. Can build #
#             children based off of what can move, and can return #
#             a heuristic value.                                  #
##################################################################$
class Node:
  def __init__(self):
    self.board = []
    self.pieces = []
    self.children = []
    self.parent = None
	  #min = -1, max = 1
    self.mmtype = 0
    #white=0 black=1
    self.blackwhite = 0
    self.depth = 0
    self.movethatgotmehere = None
    self.kingrank = 0
    self.kingfile = 0
  def __hash__(self):
    return str(self.board).__hash__()

  def heuristicValue(self):
    retval = 0
    for a in self.pieces:
      if a.getOwner() == self.blackwhite:
        if a.getType() == ord('Q'):
          retval+=9
        elif a.getType() == ord('R'):
          retval+=5
        elif a.getType() == ord('B'):
          retval+=5
        elif a.getType() == ord('N'):
          retval+=3
        elif a.getType() == ord('P'):
          retval+=1
      else:
        if a.getType() == ord('Q'):
          retval-=9
        elif a.getType() == ord('R'):
          retval-=5
        elif a.getType() == ord('B'):
          retval-=5
        elif a.getType() == ord('N'):
          retval-=3
        elif a.getType() == ord('P'):
          retval-=1
        
    return retval

  def buildchildren(self):
#    print "Building the children for", self.blackwhite
    for a in whatCanMove(self.board, self.blackwhite, self.pieces, self.kingrank, self.kingfile):
      self.children.append(createChild(self.board, self.pieces, a, self.blackwhite * -1 + 1, self.mmtype * -1, self.depth + 1))
      self.children[-1].parent = self
    return self.children


###################################################################
#Class: valToChild                                                #
#Description: Connects a node to a logical heuristic/utility value#
#             and depending on whether its a min node or a max    #
#             node decides to use greater than or less than for   #
#             __lt__ to be used in a sorting algorithm.           #
##################################################################$
class valToChild:
  def __init__(self, v, c, mm):
    self.value = v
    self.child = c
    self.mm = mm
  def __lt__(self, other):
    if self.mm == -1:
      return self.value < other.value
    if self.mm == 1:
      return self.value > other.value
  def __le__(self, other):
    if self.mm == -1:
      return self.value <= other.value
    if self.mm == 1:
      return self.value >= other.value


###################################################################
#Function: maximumValue()                                         #
#Returns: The most logical min value using the iterative deepening#
#         depth limited minimax algorithm.                        #
#Description: This finds the best value for the max player        #
#Arguments: Max Value                                             #
##################################################################$
  
def maximumValue(node, depth, tts):
  #If we reach the depth limit throw out the heuristic value
  if depth == 0:
    return node.heuristicValue()
  children = node.buildchildren()
  sortablechildren = []

  #No possible moves
  if len(children) == 0:
    if kingInCheck(node.board, node.blackwhite, 1, 1, 1, 1, node.kingrank, node.kingfile) == True:
      #if we are maxing return max int
      if node.mmtype == 1:
        return sys.maxint
      #if we are minning return min int
      elif node.mmtype == -1:
        return -1 * sys.maxint - 1
    #Kings not in check, so it's a stale mate
    else:
      return 0
  else:
    #3 repeated board states lol clusterfuck
    if node.parent is not None:
      pstate = node.parent.board
      cstate = node.board
      if node.parent.parent is not None and node.parent.parent.board == cstate:
        if node.parent.parent.parent is not None and node.parent.parent.parent.board == pstate:
          if node.parent.parent.parent.parent is not None and node.parent.parent.parent.parent.board == cstate:
            if node.parent.parent.parent.parent.parent is not None and node.parent.parent.parent.parent.parent.board == pstate:
              return 0
    #Just kings
    if len(node.pieces) == 2 and node.pieces[0].getType() == ord('K') and node.pieces[1].getType() == ord('K'):
      return 0
    #2 kings and either 1 knight or 1 bishop
    elif len(node.pieces) == 3:
      if node.pieces[0].getType() == ord('K'): 
        if node.pieces[1].getType() == ord('K'):
          if node.pieces[2].getType() == ord('B') or node.pieces[2].getType() == ord('N'):
            return 0
        if node.pieces[1].getType() == ord('B') or node.pieces[1].getType() == ord('N'):
          if node.pieces[2].getType() == ord('K'):
            return 0
      if node.pieces[0].getType() == ord('B') or node.pieces[0].getType() == ord('N'):
        if node.pieces[1].getType() == ord('K'):
          if node.pieces[2].getType() == ord('K'):
            return 0
    #2 kings and 2 bishops on the same color
    if len(node.pieces) == 4:
      kings = []
      bishops = []
      for a in node.pieces:
        if a.getType() == ord('K'):
          kings.append(True)
        if a.getType() == ord('B'):
          bishops.append(node.pieces.index(a))
      
        if len(kings) == 2 and len(bishops) == 2:
          if node.pieces[bishops[0]].getRank()%2 == node.pieces[bishops[1]].getRank()%2 \
             and node.pieces[bishops[1]].getFile()%2 == node.pieces[bishops[0]].getFile()%2:
            return 0
 
     #50 move stalemate, without pawn advancement or piece capture
     #tts gets passed in (AI.TurnsToStalemate()) from run to IDDLMM to DLMM to MinV to MaxV so we
     #don't have to iterate 50 each depth.
    temp = node
    for i in range(tts, -1, -1):
      if i == 0:
        return 0
      elif temp.parent is not None and temp.movethatgotmehere[0].getType() != ord('P') and len(temp.parent.pieces) > len(temp.pieces):
        tts = 50
        break     
  for a in children:
    sortablechildren.append(valToChild(minimumValue(a, depth - 1, tts), a, 1))
  
  sortablechildren.sort()
  while sortablechildren[-1].value != sortablechildren[0].value:
    sortablechildren.pop()
  
  randomsilly = random.randint(0, len(sortablechildren) - 1)
  return sortablechildren[randomsilly].value

###################################################################
#Function: minimumValue()                                         #
#Returns: The most logical min value using the iterative deepening#
#         depth limited minimax algorithm.                        #
#Description: This finds the best value for the min player        #
#Arguments: Min Value                                             #
##################################################################$
def minimumValue(node, depth, tts):
  #If we reach the depth limit throw out the heuristic value
  if depth == 0:
    return node.heuristicValue()
  children = node.buildchildren()
  sortablechildren = []
  
  #No possible moves
  if len(children) == 0:
    #And the king is in check
    if kingInCheck(node.board, node.blackwhite, 1, 1, 1, 1, node.kingrank, node.kingfile) == True:
      #if we are maxing return max int
      if node.mmtype == 1:
        return sys.maxint
      #if we are minning return min int
      elif node.mmtype == -1:
        return -1 * sys.maxint - 1
    #Kings not in check, so it's a stale mate
    else:
      return 0
  else:
    #3 repeated board states lol clusterfuck
    if node.parent is not None:
      pstate = node.parent.board
      cstate = node.board
      if node.parent.parent is not None and node.parent.parent.board == cstate:
        if node.parent.parent.parent is not None and node.parent.parent.parent.board == pstate:
          if node.parent.parent.parent.parent is not None and node.parent.parent.parent.parent.board == cstate:
            if node.parent.parent.parent.parent.parent is not None and node.parent.parent.parent.parent.parent.board == pstate:
              return 0
    #Just kings
    if len(node.pieces) == 2 and node.pieces[0].getType() == ord('K') and node.pieces[1].getType() == ord('K'):
      return 0
    #2 kings and either 1 knight or 1 bishop
    elif len(node.pieces) == 3:
      if node.pieces[0].getType() == ord('K'): 
        if node.pieces[1].getType() == ord('K'):
          if node.pieces[2].getType() == ord('B') or node.pieces[2].getType() == ord('N'):
            return 0
        if node.pieces[1].getType() == ord('B') or node.pieces[1].getType() == ord('N'):
          if node.pieces[2].getType() == ord('K'):
            return 0
      if node.pieces[0].getType() == ord('B') or node.pieces[0].getType() == ord('N'):
        if node.pieces[1].getType() == ord('K'):
          if node.pieces[2].getType() == ord('K'):
            return 0
    #2 kings and 2 bishops on the same color
    if len(node.pieces) == 4:
      kings = []
      bishops = []
      for a in node.pieces:
        if a.getType() == ord('K'):
          kings.append(True)
        if a.getType() == ord('B'):
          bishops.append(node.pieces.index(a))
      
        if len(kings) == 2 and len(bishops) == 2:
          if node.pieces[bishops[0]].getRank()%2 == node.pieces[bishops[1]].getRank()%2 \
             and node.pieces[bishops[1]].getFile()%2 == node.pieces[bishops[0]].getFile()%2:
            return 0
     
     #50 move stalemate, without pawn advancement or piece capture
     #tts gets passed in (AI.TurnsToStalemate()) from run to IDDLMM to DLMM to MinV to MaxV so we
     #don't have to iterate 50 each depth.

    temp = node
    for i in range(tts, -1, -1):
      if i == 0:
        return 0
      elif temp.parent is not None and temp.movethatgotmehere[0].getType() != ord('P') and len(temp.parent.pieces) > len(temp.pieces):
        tts = 50
        break
  #Builds all the children
  for a in children:
    sortablechildren.append(valToChild(maximumValue(a, depth - 1, tts), a, -1))
  
  #Sorts them by heuristic/utility value
  sortablechildren.sort()
  #Get rid of all the ones that are not a min
  while sortablechildren[-1].value != sortablechildren[0].value:
    sortablechildren.pop()
  #Pick a random one
  randomsilly = random.randint(0, len(sortablechildren) - 1)
  #Return its value
  return sortablechildren[randomsilly].value

##################################################################
#Function: DLMM                                                  #
#Returns: A move                                                 #
#Description: Runs minimax to the desired depth.                 #
#Arguments: The root node, the depth limit and turns to stalemate#
##################################################################
def DLMM(node, depth, tts):
  children = node.buildchildren()
  sortablechildren = []

  for a in children:
    sortablechildren.append(valToChild(minimumValue(a, depth - 1, tts), a, 1))
   
  sortablechildren.sort()
  while sortablechildren[-1].value != sortablechildren[0].value:
    sortablechildren.pop()
  randomsilly = random.randint(0, len(sortablechildren) - 1)
  return sortablechildren[randomsilly].child.movethatgotmehere

##################################################################
#Function: IDDLMM                                                #
#Returns: The most logical move using the iterative deepening    #
#         depth limited minimax algorithm.                       #
#Description: This starts the move finding algorithm, it starts  #
#             with the root node, and builds a game tree to      #
#             choose a logical move.                             #
#Arguments: The current board state, the current pieces, which   #
#           player we are running the algorithm for, the max     #
#           depth to run to, the kings rank and file, and the num#
#           of turns til there is a stalemate.                   #
##################################################################
def IDDLMM(board, pieces, player, maxdepth, kr, kf, tts):
  move = None
  startnode = Node()
  startnode.board = board
  startnode.pieces = pieces
  startnode.kingrank = kr
  startnode.kingfile = kf
  startnode.mmtype = 1
  startnode.depth = 1
  startnode.blackwhite = player
  for i in range(1, maxdepth+1):
    startnode.children = []
    move = DLMM(startnode, i, tts)
  return move

##################################################################
#Function: rankFileTransform()                                   #
#Returns: server rank and file transformed to my rank and file   #
##################################################################
def rankFileTransform(r, f):
  return [r * -1 + 8, f + 1]
   
class AI(BaseAI):
  """The class implementing gameplay logic."""
  board = []
  enpassants = []
  kingfile = 0
  kingrank = 0
  kingchar = ' '
  lower = 0
  upper = 1
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"
  ###################################################################
  #Function: buildBoard()                                           #
  #Description: This is ran at the beginning of run() everytime to  #
  #             get a usable representation of the current state of #
  #             the game.                                           #
  ###################################################################
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
      if p.getOwner() == self.playerID() and chr(p.getType()).upper() == 'K':
        self.kingfile = p.getFile() - 1
        self.kingrank = p.getRank() * -1 + 8
        if p.getOwner() == 0:
          self.kingchar == 'k'
        else:
          self.kingchar == 'K'
      if p.getOwner() == 0:
        self.board[p.getRank() * -1 + 8][p.getFile() - 1] = str.lower(chr(p.getType()))
      else:
        self.board[p.getRank() * -1 + 8][p.getFile() - 1] = chr(p.getType())

  def printBoard(self):
    str = ""
    for a in self.board:
      for b in a:
        str+=b
      str+='\n'
    print str

  def init(self):
    #Begin our nice pretty output
    print "From\tTo"

  def end(self):
    pass

  def run(self):
    #First build my board, so I can tell where everything is
    self.buildBoard()
    self.printBoard()
    moves = whatCanMove(self.board, self.playerID(), self.pieces, self.kingrank, self.kingfile)
    mover = moves[random.randint(0, len(moves)-1)]
    #Pawn promotion
    if len(mover) >= 3 and mover[2] != '':
      mover[0].move(mover[1][1], mover[1][0], ord(mover[2]))
    else:
      mover[0].move(mover[1][1], mover[1][0], 0)

    #Nice pretty output
    string = ''
    string += chr(ord('a') + mover[0].getFile() - 1)
    string += str(mover[0].getRank())
    string += '\t'
    string += chr(ord('a') + mover[1][1] - 1)
    string += str(mover[1][0])
    print string
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
