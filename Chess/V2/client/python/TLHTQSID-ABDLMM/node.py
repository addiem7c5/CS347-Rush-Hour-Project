#ADDIE MARTIN
#CS347
#node.py
WHITE = 0
BLACK = 1
LOWERCASE = 0
UPPERCASE = 1

#Everything needed for a Node in ABMM
class Node:
  #Constructor
  def __init__(self, board, movedpieces, player, tts = 100, parent = None, move = None):
    self.board = board
    self.movedpieces = movedpieces
    self.player = player
    self.parent = parent
    self.movethatgotmehere = move
    self.turnstostalemate = tts
  
  #String Representation of a State
  def __str__(self):
    outstr = "Player " + str(self.player) + "\n"
    outstr += "WROM: " + str(self.movedpieces[0]) + " WR7M: " + str(self.movedpieces[1])\
                       + " WKM: " + str(self.movedpieces[2]) + "\n"
    outstr += "BROM: " + str(self.movedpieces[3]) + " BR7M: " + str(self.movedpieces[4])\
                       + " BKM: " + str(self.movedpieces[5]) + "\n"
    outstr = ""
    for a in self.board:
      for b in a:
        outstr += b
      outstr += '\n'
    outstr += "Heuristic Value: "
    outstr += str(self.heuristicValue()) 
    outstr += '\n'
    return outstr
  
  def __hash__(self):
    return str(self.board).__hash__()
  
  def printMTGMH(self):
    print chr(ord('a') + self.movethatgotmehere[1]) + str(self.movethatgotmehere[0] * -1 + 8) + ' ' + chr(ord('a') + self.movethatgotmehere[3]) + str(self.movethatgotmehere[2] * -1 + 8)
  
  #A state is quiescent if there was a capture to get to it
  def quiescenceHeuristicValue(self):
    if self.parent == None:
      return True
    
    pflattenedboard = [item for sublist in self.parent.board for item in sublist]
    sflattenedboard = [item for sublist in self.board for item in sublist]
    if pflattenedboard.count('.') < sflattenedboard.count('.'):
      return False
    return True

  #Material Heuristic + other players king in check
  def heuristicValue(self):
    value = 0
    
    for a in self.board:
      for b in a:
        if b == 'q':
          value += 9
        if b == 'r':
          value += 5
        if b == 'b':
          value += 5
        if b == 'n':
          value += 3
        if b == 'p':
          value += 1
        if b == 'Q':
          value -= 9
        if b == 'R':
          value -= 5
        if b == 'B':
          value -= 5
        if b == 'N':
          value -= 3
        if b == 'P':
          value -= 1
    
    if self.kingInCheck(1, 1, 1, 1, True) and self.player == 0:
      value += 15
    elif self.kingInCheck(1, 1, 1, 1, True) and self.player == 1:
      value -= 15
    return value
  
  #Seeing if a king is check by moving the piece at r1,f1 to r2,f2
  def kingInCheck(self, r1, f1, r2, f2, otherPlayer = False):
    tempboard = []
    kingrank = -1
    kingfile = -1
    for a in self.board:
      temp = []
      for b in a:
        if b in 'kK' and b.isupper() == self.player and not otherPlayer:
          kingrank = self.board.index(a)
          kingfile = a.index(b)
        elif b in 'kK' and otherPlayer:
          kingrank = self.board.index(a)
          kingfile = a.index(b)
        temp.append(b)
      tempboard.append(temp)

    if tempboard[r1][f1] in 'Pp':
      if abs(r1 - r2) == 2 and abs(f1 - f2) == 1:
        if r1 > r2:
          tempboard[r2 - 1][f2] = '.'
        elif r2 > r1:
          tempboard[r2 + 1][f2] = '.'
    
    if r1 == kingrank and f1 == kingfile:
      kingrank = r2
      kingfile = f2

    tempboard[r2][f2] = tempboard[r1][f1]
    tempboard[r1][f1] = '.'

    Down = False
    Up = False
    Right = False
    Left = False
    #Pawn
    if self.player == 0 or (self.player == 1 and otherPlayer):
      if kingrank - 1 >= 0:
        if kingfile - 1 >= 0:
          if self.board[kingrank - 1][kingfile - 1] == 'P':
            return True
        if kingfile + 1 <= 7:
          if self.board[kingrank - 1][kingfile + 1] == 'P':
            return True
    else:
      if kingrank + 1 <= 7:
        if kingfile - 1 >= 0:
          if self.board[kingrank + 1][kingfile - 1] == 'p':
            return True
        if kingfile + 1 <= 7:
          if self.board[kingrank + 1][kingfile + 1] == 'p':
            return True

    #King
    if kingrank + 1 <= 7:
      if tempboard[kingrank + 1][kingfile] != '.' and \
         tempboard[kingrank + 1][kingfile].isupper() != tempboard[kingrank][kingfile].isupper() and \
         tempboard[kingrank + 1][kingfile] in 'Kk':
        return True
      if kingfile + 1 <= 7 and tempboard[kingrank + 1][kingfile + 1] != '.' and \
         tempboard[kingrank + 1][kingfile + 1].isupper() != tempboard[kingrank][kingfile].isupper() and \
         tempboard[kingrank + 1][kingfile + 1] in 'Kk':
        return True
      if kingfile - 1 >= 0 and tempboard[kingrank + 1][kingfile - 1] != '.' and \
         tempboard[kingrank + 1][kingfile - 1].isupper() != tempboard[kingrank][kingfile].isupper() and \
         tempboard[kingrank + 1][kingfile - 1] in 'Kk':
        return True
    if kingrank - 1 >= 0:
      if tempboard[kingrank - 1][kingfile] != '.' and \
         tempboard[kingrank - 1][kingfile].isupper() != tempboard[kingrank][kingfile].isupper() and \
         tempboard[kingrank - 1][kingfile] in 'Kk':
        return True
      if kingfile + 1 <= 7 and tempboard[kingrank - 1][kingfile + 1] != '.' and \
         tempboard[kingrank - 1][kingfile + 1].isupper() != tempboard[kingrank][kingfile].isupper() and \
         tempboard[kingrank - 1][kingfile + 1] in 'Kk':
        return True
      if kingfile - 1 >= 0 and tempboard[kingrank - 1][kingfile - 1] != '.' and \
         tempboard[kingrank - 1][kingfile - 1].isupper() != tempboard[kingrank][kingfile].isupper() and \
         tempboard[kingrank - 1][kingfile - 1] in 'Kk':
        return True
    if kingfile - 1 >= 0 and tempboard[kingrank][kingfile - 1] != '.' and \
       tempboard[kingrank][kingfile - 1].isupper() != tempboard[kingrank][kingfile].isupper() and \
       tempboard[kingrank][kingfile - 1] in 'Kk':
      return True
    if kingfile + 1 <= 7 and tempboard[kingrank][kingfile + 1] != '.' and \
       tempboard[kingrank][kingfile + 1].isupper() != tempboard[kingrank][kingfile].isupper() and \
       tempboard[kingrank][kingfile + 1] in 'Kk':
      return True
    #Rook or Queen  
    for i in range(1, 8):
      if kingrank + i <= 7:
        if not Down and tempboard[kingrank + i][kingfile] != '.' and \
           tempboard[kingrank + i][kingfile].isupper() != tempboard[kingrank][kingfile].isupper() and \
           tempboard[kingrank + i][kingfile] in 'QqRr':
          return True
        elif tempboard[kingrank + i][kingfile] != '.' and \
             tempboard[kingrank + i][kingfile].isupper() == tempboard[kingrank][kingfile].isupper():
          Down = True
      if kingrank - i >= 0:
        if not Up and tempboard[kingrank - i][kingfile] != '.' and \
           tempboard[kingrank - i][kingfile].isupper() != tempboard[kingrank][kingfile].isupper() and \
           tempboard[kingrank - i][kingfile] in 'QqRr':
          return True
        elif tempboard[kingrank - i][kingfile] != '.' and \
             tempboard[kingrank - i][kingfile].isupper() == tempboard[kingrank][kingfile].isupper():
          Up = True
      if kingfile + i <= 7:
        if not Right and tempboard[kingrank][kingfile + i] != '.' and \
           tempboard[kingrank][kingfile + i].isupper() != tempboard[kingrank][kingfile].isupper() and \
           tempboard[kingrank][kingfile + i] in 'QqRr':
          return True
        elif tempboard[kingrank][kingfile + i] != '.' and \
             tempboard[kingrank][kingfile + i].isupper() == tempboard[kingrank][kingfile].isupper():
          Right = True
      if kingfile - i >= 0:
        if not Left and tempboard[kingrank][kingfile - i] != '.' and \
           tempboard[kingrank][kingfile - i].isupper() != tempboard[kingrank][kingfile].isupper() and \
           tempboard[kingrank][kingfile - i] in 'QqRr':
          return True
        elif tempboard[kingrank][kingfile - i] != '.' and \
             tempboard[kingrank][kingfile - i].isupper() == tempboard[kingrank][kingfile].isupper():
          Left = True
      if Up and Down and Left and Right:
        break

    Downright = False
    Downleft = False
    Upleft = False
    Upright = False
    for i in range(1, 8):
      if kingrank + i <= 7 and kingfile + i <= 7:
        if not Downright and tempboard[kingrank + i][kingfile + i] != '.' and \
           tempboard[kingrank + i][kingfile + i].isupper() != tempboard[kingrank][kingfile].isupper() and \
           tempboard[kingrank + i][kingfile + i] in 'QqBb':
          return True
        elif tempboard[kingrank + i][kingfile + i] != '.' and \
             tempboard[kingrank + i][kingfile + i].isupper() == tempboard[kingrank][kingfile].isupper():
          Downright = True
      if kingrank + i <= 7 and kingfile - i >= 0:
        if not Downleft and tempboard[kingrank + i][kingfile - i] != '.' and \
           tempboard[kingrank + i][kingfile - i].isupper() != tempboard[kingrank][kingfile].isupper() and \
           tempboard[kingrank + i][kingfile - i] in 'QqBb':
          return True
        elif tempboard[kingrank + i][kingfile - i] != '.' and \
             tempboard[kingrank + i][kingfile - i].isupper() == tempboard[kingrank][kingfile].isupper():
          Downleft = True
      if kingrank - i >= 0 and kingfile - i >= 0:
        if not Upleft and tempboard[kingrank - i][kingfile - i] != '.' and \
           tempboard[kingrank - i][kingfile - i].isupper() != tempboard[kingrank][kingfile].isupper() and \
           tempboard[kingrank - i][kingfile - i] in 'QqBb':
          return True
        elif tempboard[kingrank - i][kingfile - i] != '.' and \
             tempboard[kingrank - i][kingfile - i].isupper() == tempboard[kingrank][kingfile].isupper():
          Upleft = True
      if kingrank - i >= 0 and kingfile + i <= 7:
        if not Upright and tempboard[kingrank - i][kingfile + i] != '.' and \
           tempboard[kingrank - i][kingfile + i].isupper() != tempboard[kingrank][kingfile].isupper() and \
           tempboard[kingrank - i][kingfile + i] in 'QqBb':
          return True
        elif tempboard[kingrank - i][kingfile + i] != '.' and \
             tempboard[kingrank - i][kingfile + i].isupper() == tempboard[kingrank][kingfile].isupper():
          Upright = True
      if Upright and Upleft and Downright and Downleft:
        break

    if kingrank - 2 >= 0:
      if kingfile - 1 >= 0:
        if tempboard[kingrank - 2][kingfile - 1] in 'Nn' and \
           tempboard[kingrank - 2][kingfile - 1].isupper() != tempboard[kingrank][kingfile].isupper():
          return True
      if kingfile + 1 <= 7:
        if tempboard[kingrank - 2][kingfile + 1] in 'Nn' and \
           tempboard[kingrank - 2][kingfile + 1].isupper() != tempboard[kingrank][kingfile].isupper():
          return True
    if kingrank + 2 <= 7:
      if kingfile - 1 >= 0:
        if tempboard[kingrank + 2][kingfile - 1] in 'Nn' and \
           tempboard[kingrank + 2][kingfile - 1].isupper() != tempboard[kingrank][kingfile].isupper():
          return True
      if kingfile + 1 <= 7:
        if tempboard[kingrank + 2][kingfile + 1] in 'Nn' and \
           tempboard[kingrank + 2][kingfile + 1].isupper() != tempboard[kingrank][kingfile].isupper():
          return True

    if kingfile - 2 >= 0:
      if kingrank - 1 >= 0:
        if tempboard[kingrank - 1][kingfile - 2] in 'Nn' and \
           tempboard[kingrank - 1][kingfile - 2].isupper() != tempboard[kingrank][kingfile].isupper():
          return True
      if kingrank + 1 <= 7:
        if tempboard[kingrank + 1][kingfile - 2] in 'Nn' and \
           tempboard[kingrank + 1][kingfile - 2].isupper() != tempboard[kingrank][kingfile].isupper():
          return True
    if kingfile + 2 <= 7:
      if kingrank - 1 >= 0:
        if tempboard[kingrank - 1][kingfile + 2] in 'Nn' and \
           tempboard[kingrank - 1][kingfile + 2].isupper() != tempboard[kingrank][kingfile].isupper():
          return True
      if kingrank + 1 <= 7:
        if tempboard[kingrank + 1][kingfile + 2] in 'Nn' and \
           tempboard[kingrank + 1][kingfile + 2].isupper() != tempboard[kingrank][kingfile].isupper():
          return True

    if tempboard[kingrank][kingfile].lower() == True:
      if kingrank - 1 >= 0:
        if kingfile - 1 >= 0 and tempboard[kingrank-1][kingfile-1] == 'P':
          return True
        if kingfile + 1 <= 7 and tempboard[kingrank-1][kingfile+1] == 'P':
          return True
    else:
      if kingrank + 1 <= 7:
        if kingfile - 1 >= 0 and tempboard[kingrank+1][kingfile-1] == 'p':
          return True
        if kingfile + 1 <= 7 and tempboard[kingrank+1][kingfile+1] == 'p':
          return True

    return False

  #All the King Moves
  def kingMoves(self, r, f):
    moves = []
    if r + 1 <= 7:
      if self.board[r+1][f] == '.' or (self.board[r+1][f] != '.' and self.board[r+1][f].islower() != self.board[r][f].islower()):
        if not self.kingInCheck(r, f, r+1, f):
          moves.append([r, f, r+1, f])
      if f + 1 <= 7:
        if self.board[r+1][f+1] == '.' or (self.board[r+1][f+1] != '.' and self.board[r+1][f+1].islower() != self.board[r][f].islower()):
          if not self.kingInCheck(r, f, r+1, f+1):
            moves.append([r, f, r+1, f+1])
      if f - 1 >= 0:
        if self.board[r+1][f-1] == '.' or (self.board[r+1][f-1] != '.' and self.board[r+1][f-1].islower() != self.board[r][f].islower()):
          if not self.kingInCheck(r, f, r+1, f-1):
            moves.append([r, f, r+1, f-1])
    if r - 1 >= 0:
      if self.board[r-1][f] == '.' or (self.board[r-1][f] != '.' and self.board[r-1][f].islower() != self.board[r][f].islower()):
        if not self.kingInCheck(r, f, r-1, f):
          moves.append([r, f, r-1, f])
      if f + 1 <= 7:
        if self.board[r-1][f+1] == '.' or (self.board[r-1][f+1] != '.' and self.board[r-1][f+1].islower() != self.board[r][f].islower()):
          if not self.kingInCheck(r, f, r-1, f+1):
            moves.append([r, f, r-1, f+1])
      if f - 1 >= 0:
        if self.board[r-1][f-1] == '.' or (self.board[r-1][f-1] != '.' and self.board[r-1][f-1].islower() != self.board[r][f].islower()):
          if not self.kingInCheck(r, f, r-1, f-1):
            moves.append([r, f, r-1, f-1])
    if f - 1 >= 0:
      if self.board[r][f-1] == '.' or (self.board[r][f-1] != '.' and self.board[r][f-1].islower() != self.board[r][f].islower()):
        if not self.kingInCheck(r, f, r, f-1):
          moves.append([r, f, r, f-1])
    if f + 1 <= 7:
      if self.board[r][f+1] == '.' or (self.board[r][f+1] != '.' and self.board[r][f+1].islower() != self.board[r][f].islower()):
        if not self.kingInCheck(r, f, r, f+1):
          moves.append([r, f, r, f+1])

    if self.player == 0:
      if self.movedpieces[0] == False and self.movedpieces[2] == False:
        if self.board[r][f-1] == '.' and self.board[r][f-2] == '.' and not \
           self.kingInCheck(r, f, r, f-1) and not self.kingInCheck(r, f, r, f-2):
          moves.append([r, f, r, f-2])
      if self.movedpieces[1] == False and self.movedpieces[2] == False:
        if self.board[r][f+1] == '.' and self.board[r][f+2] == '.' and not \
           self.kingInCheck(r, f, r, f+1) and not self.kingInCheck(r, f, r, f+2):
          moves.append([r, f, r, f+2])
    if self.player == 1:
      if self.movedpieces[3] == False and self.movedpieces[5] == False:
        if self.board[r][f-1] == '.' and self.board[r][f-2] == '.' and not \
           self.kingInCheck(r, f, r, f-1) and not self.kingInCheck(r, f, r, f-2):
          moves.append([r, f, r, f-2])
      if self.movedpieces[4] == False and self.movedpieces[5] == False:
        if self.board[r][f+1] == '.' and self.board[r][f+2] == '.' and not \
           self.kingInCheck(r, f, r, f+1) and not self.kingInCheck(r, f, r, f+2):
          moves.append([r, f, r, f+2])
    return moves

  #All the Rook Moves
  def rookMoves(self, r, f):
    moves = []
    Down = False
    Left = False
    Up = False
    Right = False

    for i in range(1, 8):
      if r + i <= 7 and not Down:
        if (self.board[r+i][f] == '.' or \
           (self.board[r+i][f] != '.' and self.board[r+i][f].isupper() != self.board[r][f].isupper())) \
           and not self.kingInCheck(r, f, r+i, f):
          moves.append([r, f, r+i, f])
          if self.board[r+i][f] != '.': Down = True
        elif self.board[r+i][f] != '.' and self.board[r+i][f].isupper() == self.board[r][f].isupper():
          Down = True
      if r - i >= 0 and not Up:
        if (self.board[r-i][f] == '.' or \
           (self.board[r-i][f] != '.' and self.board[r-i][f].isupper() != self.board[r][f].isupper())) \
           and not self.kingInCheck(r, f, r-i, f):
          moves.append([r, f, r-i, f])
          if self.board[r-i][f] != '.': Up = True
        elif self.board[r-i][f] != '.' and self.board[r-i][f].isupper() == self.board[r][f].isupper():
          Up = True
      if f + i <= 7 and not Right:
        if (self.board[r][f+i] == '.' or \
           (self.board[r][f+i] !=  '.' and self.board[r][f+i].isupper() != self.board[r][f].isupper())) \
           and not self.kingInCheck(r, f, r, f+i):
          moves.append([r, f, r, f+i])
          if self.board[r][f+i] != '.': Right = True
        elif self.board[r][f+i] !=  '.' and self.board[r][f+i].isupper() == self.board[r][f].isupper():
          Right = True
      if f - i >= 0 and not Left:
        if (self.board[r][f-i] == '.' or \
           (self.board[r][f-i] != '.' and self.board[r][f-i].isupper() != self.board[r][f].isupper())) \
           and not self.kingInCheck(r, f, r, f-i):
          moves.append([r, f, r, f-i])
          if self.board[r][f-i] != '.': Left = True
        elif self.board[r][f-i] != '.' and self.board[r][f-i].isupper() == self.board[r][f].isupper():
          Left = True
      if Up and Right and Left and Down:
        break

    return moves

  #All the Bishop Moves
  def bishopMoves(self, r, f):
    moves = []
    DownRight = False
    DownLeft = False
    UpLeft = False
    UpRight = False

    for i in range(1, 8):
      if r + i <= 7 and f + i <= 7 and not DownRight:
        if (self.board[r+i][f+i] == '.' or \
           (self.board[r+i][f+i] != '.' and self.board[r+i][f+i].isupper() != self.board[r][f].isupper())) \
           and not self.kingInCheck(r, f, r+i, f+i):
          moves.append([r, f, r+i, f+i])
          DownRight = True
          if self.board[r+i][f+i] != '.': DownRight = True
        elif self.board[r+i][f+i] != '.' and self.board[r+i][f+i].isupper() == self.board[r][f].isupper():
          DownRight = True
      if r - i >= 0 and f - i >= 0 and not UpLeft:
        if (self.board[r-i][f-i] == '.' or \
           (self.board[r-i][f-i] != '.' and self.board[r-i][f-i].isupper() != self.board[r][f].isupper())) \
           and not self.kingInCheck(r, f, r-i, f-i):
          moves.append([r, f, r-i, f-i])
          UpLeft = True
          if self.board[r-i][f-i] != '.': UpLeft = True
        elif self.board[r-i][f-i] != '.' and self.board[r-i][f-i].isupper() == self.board[r][f].isupper():
          UpLeft = True
      if f + i <= 7 and r - i >= 0 and not UpRight:
        if (self.board[r-i][f+i] == '.' or \
           (self.board[r-i][f+i] !=  '.' and self.board[r-i][f+i].isupper() != self.board[r][f].isupper())) \
           and not self.kingInCheck(r, f, r-i, f+i):
          moves.append([r, f, r-i, f+i])
          UpRight = True
          if self.board[r-i][f+i] != '.': UpRight = True
        elif self.board[r-i][f+i] !=  '.' and self.board[r-i][f+i].isupper() == self.board[r][f].isupper():
          UpRight = True
      if f - i >= 0 and r + i <= 7 and not DownLeft:
        if (self.board[r+i][f-i] == '.' or \
           (self.board[r+i][f-i] != '.' and self.board[r+i][f-i].isupper() != self.board[r][f].isupper())) \
           and not self.kingInCheck(r, f, r+i, f-i):
          moves.append([r, f, r+i, f-i])
          DownLeft = True
          if self.board[r+i][f-i] != '.': DownLeft = True
        elif self.board[r+i][f-i] != '.' and self.board[r+i][f-i].isupper() == self.board[r][f].isupper():
          DownLeft = True
      if UpLeft and UpRight and DownLeft and DownRight:
        break

    return moves

  #All the Knight Moves
  def knightMoves(self, r, f):
    moves = []
  
    if f - 2 >= 0:
      if r - 1 >= 0 and (self.board[r-1][f-2] == '.' or \
         self.board[r-1][f-2].islower() != self.board[r][f].islower()) and \
         not self.kingInCheck(r, f, r-1, f-2):
        moves.append([r, f, r-1, f-2])
      if r + 1 <= 7 and (self.board[r+1][f-2] == '.' or \
         self.board[r+1][f-2].islower() != self.board[r][f].islower()) and \
         not self.kingInCheck(r, f, r+1, f-2):
        moves.append([r, f, r+1, f-2])
    if f + 2 <= 7:
      if r - 1 >= 0 and (self.board[r-1][f+2] == '.' or \
         self.board[r-1][f+2].islower() != self.board[r][f].islower()) and \
         not self.kingInCheck(r, f, r-1, f+2):
        moves.append([r, f, r-1, f+2])
      if r + 1 <= 7 and (self.board[r+1][f+2] == '.' or \
         self.board[r+1][f+2].islower() != self.board[r][f].islower()) and \
         not self.kingInCheck(r, f, r+1, f+2):
        moves.append([r, f, r+1, f+2])
    
    if r - 2 >= 0:
      if f - 1 >= 0 and (self.board[r-2][f-1] == '.' or \
         self.board[r-2][f-1].islower() != self.board[r][f].islower()) and \
         not self.kingInCheck(r, f, r-2, f-1):
        moves.append([r, f, r-2, f-1])
      if f + 1 <= 7 and (self.board[r-2][f+1] == '.' or \
         self.board[r-2][f+1].islower() != self.board[r][f].islower()) and \
         not self.kingInCheck(r, f, r-2, f+1):
        moves.append([r, f, r-2, f+1])
    if r + 2 <= 7:
      if f - 1 >= 0 and (self.board[r+2][f-1] == '.' or \
         self.board[r+2][f-1].islower() != self.board[r][f].islower()) and \
         not self.kingInCheck(r, f, r+2, f-1):
        moves.append([r, f, r+2, f-1])
      if f + 1 <= 7 and (self.board[r+2][f+1] == '.' or \
         self.board[r+2][f+1].islower() != self.board[r][f].islower()) and \
         not self.kingInCheck(r, f, r+2, f+1):
        moves.append([r, f, r+2, f+1])

    return moves

  #All the Pawn Moves
  def pawnMoves(self, r, f):
    moves = []
    if self.player == 0:
      #pawn hasn't moved yet
      if r == 6:
        if self.board[r-1][f] == '.':
          if not self.kingInCheck(r, f, r-1, f):
            moves.append([r, f, r-1, f])
          if self.board[r-2][f] == '.' and not self.kingInCheck(r, f, r-2, f):
            moves.append([r, f, r-2, f])
        if f-1 >= 0 and self.board[r-1][f-1] != '.' and self.board[r-1][f-1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r-1, f-1):
          moves.append([r, f, r-1, f-1])
        if f+1 <= 7 and self.board[r-1][f+1] != '.' and self.board[r-1][f+1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r-1, f+1):
          moves.append([r, f, r-1, f+1])
      #ready for promotion
      elif r == 1:
        if self.board[r-1][f] == '.':
          if not self.kingInCheck(r, f, r-1, f):
            moves.append([r, f, r-1, f, ord('Q')])
            moves.append([r, f, r-1, f, ord('N')])
        if f-1 >= 0 and self.board[r-1][f-1] != '.' and self.board[r-1][f-1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r-1, f-1):
          moves.append([r, f, r-1, f-1, ord('Q')])
          moves.append([r, f, r-1, f-1, ord('N')])
        if f+1 <= 7 and self.board[r-1][f+1] != '.' and self.board[r-1][f+1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r-1, f+1):
          moves.append([r, f, r-1, f+1, ord('Q')])
          moves.append([r, f, r-1, f+1, ord('N')])
      #Regular Pawn Move
      else:
        if r-1 >= 0 and self.board[r-1][f] == '.':
          if not self.kingInCheck(r, f, r-1, f):
            moves.append([r, f, r-1, f])
        if r-1 >= 0 and f-1 >= 0 and self.board[r-1][f-1] != '.' and self.board[r-1][f-1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r-1, f-1):
          moves.append([r, f, r-1, f-1])
        if r-1 >= 0 and f+1 <= 7 and self.board[r-1][f+1] != '.' and self.board[r-1][f+1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r-1, f+1):
          moves.append([r, f, r-1, f+1])
        
    else:
      #pawn hasn't moved yet
      if r == 1:
        if self.board[r+1][f] == '.': 
          if not self.kingInCheck(r, f, r+1, f):
            moves.append([r, f, r+1, f])
          if self.board[r+2][f] == '.' and not self.kingInCheck(r, f, r+2, f):
            moves.append([r, f, r+2, f])
        if f-1 >= 0 and self.board[r+1][f-1] != '.' and self.board[r+1][f-1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r+1, f-1):
          moves.append([r, f, r+1, f-1])

        if f+1 <= 7 and self.board[r+1][f+1] != '.' and self.board[r+1][f+1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r+1, f+1):
          moves.append([r, f, r+1, f+1])
      #pawn ready to be promoted
      elif r == 6:
        if self.board[r+1][f] == '.':
          if not self.kingInCheck(r, f, r+1, f):
            moves.append([r, f, r+1, f, ord('Q')])
            moves.append([r, f, r+1, f, ord('N')])
        if f-1 >= 0 and self.board[r+1][f-1] != '.' and self.board[r+1][f-1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r+1, f-1):
          moves.append([r, f, r+1, f-1, ord('Q')])
          moves.append([r, f, r+1, f-1, ord('N')])
        if f+1 <= 7 and self.board[r+1][f+1] != '.' and self.board[r+1][f+1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r+1, f+1):
          moves.append([r, f, r+1, f+1, ord('Q')])
          moves.append([r, f, r+1, f+1, ord('N')])
      #regular pawn move
      else:
        if r+1 <= 7 and self.board[r+1][f] == '.':
          if not self.kingInCheck(r, f, r+1, f):
            moves.append([r, f, r+1, f])
        if r+1 <= 7 and f-1 >= 0 and self.board[r+1][f-1] != '.' and self.board[r+1][f-1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r+1, f-1):
          moves.append([r, f, r+1, f-1])
        if r+1 <= 7 and f+1 <= 7 and self.board[r+1][f+1] != '.' and self.board[r+1][f+1].isupper() != self.board[r][f].isupper() \
           and not self.kingInCheck(r, f, r+1, f+1):
          moves.append([r, f, r+1, f+1])
 
    return moves

  #Everything that Can move all together!
  def whatCanMove(self):
    moves = []
    
    for i in range (0, 8):
      for j in range(0, 8):
        if self.board[i][j] in 'Kk' and self.board[i][j].isupper() == self.player:
          moves += self.kingMoves(i, j)
        elif self.board[i][j] in 'Qq' and self.board[i][j].isupper() == self.player:
          moves += self.bishopMoves(i, j)
          moves += self.rookMoves(i, j)
        elif self.board[i][j] in 'Bb' and self.board[i][j].isupper() == self.player:
          moves += self.bishopMoves(i, j)
        elif self.board[i][j] in 'Nn' and self.board[i][j].isupper() == self.player:
          moves += self.knightMoves(i, j)
        elif self.board[i][j] in 'Rr' and self.board[i][j].isupper() == self.player:
          moves += self.rookMoves(i, j)
        elif self.board[i][j] in 'Pp' and self.board[i][j].isupper() == self.player:
          moves += self.pawnMoves(i, j)
    return moves

  #Applies move to current state, and returns a new board
  def applyMove(self, move):
    tempboard = []
    for a in self.board:
      temp = []
      for b in a:
        temp.append(b)
      tempboard.append(temp)

    tempboard[move[2]][move[3]] = tempboard[move[0]][move[1]]
    tempboard[move[0]][move[1]] = '.'
    
    if tempboard[move[0]][move[1]] in 'Pp':
      if abs(move[0] - move[2]) == 2 and abs(move[1] - move[3]) == 1:
        if move[0] > move[2]:
          tempboard[move[2] - 1][move[3]] = '.'
        elif move[2] > move[0]:
          tempboard[move[2] + 1][move[3]] = '.'
    return tempboard

  #Based off of what can move, this creates new nodes and returns them
  def getChildren(self):
    childrens = []
    for a in self.whatCanMove():
      newmovedpieces = []
      newnode = None
      tts = self.turnstostalemate
      for b in self.movedpieces:
        newmovedpieces.append(b)
      if self.board[a[0]][a[1]] == 'r' and a[1] == 0:
        newmovedpieces[0] = True
      if self.board[a[0]][a[1]] == 'r' and a[1] == 7:
        newmovedpieces[1] = True
      if self.board[a[0]][a[1]] == 'k':
        newmovedpieces[2] = True
      if self.board[a[0]][a[1]] == 'R' and a[1] == 0:
        newmovedpieces[3] = True
      if self.board[a[0]][a[1]] == 'R' and a[1] == 7:
        newmovedpieces[4] = True
      if self.board[a[0]][a[1]] == 'K':
        newmovedpieces[5] = True
      
      tts -= 1
      if self.board[a[0]][a[1]] in 'pP' or self.board[a[2]][a[3]] != '.':
        tts = 100
      newnode = Node(self.applyMove(a), newmovedpieces, self.player * -1 + 1, tts, self, a)
      childrens.append(newnode)
    return childrens
