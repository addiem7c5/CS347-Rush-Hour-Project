#-*-python-*-
#ADDIE MARTIN
#CS347
#AI.py
from BaseAI import BaseAI
from GameObject import *
from node import Node
import random
import os
import time
import sys
import math
import operator 

WHITE = 0
BLACK = 1
LOWERCASE = 0
UPPERCASE = 1

###################################################################
#Class: ValToChild                                                #
#Description: Connects a node to a logical heuristic/utility value#
#             and depending on whether its a min node or a max    #
#             node decides to use greater than or less than for   #
#             __lt__ to be used in a sorting algorithm.           #
##################################################################$
class ValToChild:
  def __init__(self, v, c):
    self.value = v
    self.child = c
  def __lt__(self, other):
    if self.mm == 1:
      return self.value > other.value
  def __le__(self, other):
    if self.mm == 1:
      return self.value >= other.value 

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"


  #Avg moves = 50. This gives little time at beginning and end, but alot in the middle.
  #Divides it up into 50 even moves 
  def timeHeuristic(self, movenumber):
    return -17.5 * math.cos(3.14159265/50.0 * float(movenumber/2)) + 18.0

  #Builds a node based off of info from the server
  def buildRootNode(self):
    board = []
    whiterookfile0moved = True
    whiterookfile7moved = True
    whitekingmoved = True
    blackrookfile0moved = True
    blackrookfile7moved = True
    blackkingmoved = True
    for i in range(0, 8):
      temp = []
      for j in range(0, 8):
        temp.append('.')
      board.append(temp)
 
    for a in self.pieces:
      if a.getOwner() == WHITE:
        board[a.getRank() * -1 + 8][a.getFile() - 1] = chr(a.getType()).lower()
        if a.getType() == ord('R'):
          if a.getHasMoved() == False:
            if a.getFile() == 1:
              whiterookfile0moved = False
            if a.getFile() == 8:
              whiterookfile7moved = False
        if a.getType() == ord('K'):
          if a.getHasMoved() == False:
            whitekingmoved = False
      else:
        board[a.getRank() * -1 + 8][a.getFile() - 1] = chr(a.getType())
        if a.getType() == ord('R'):
          if a.getHasMoved() == False:
            if a.getFile() == 1:
              blackrookfile0moved = False
            if a.getFile() == 8:
              blackrookfile7moved = False
        if a.getType() == ord('K'):
          if a.getHasMoved() == False:
            blackkingmoved = False
 
    newNode = Node(board, [whiterookfile0moved, whiterookfile7moved, whitekingmoved, \
                           blackrookfile0moved, blackrookfile7moved, blackkingmoved],\
                          self.playerID(), self.TurnsToStalemate())
    
    return newNode
    
  def init(self):
    self.historytable = {}
    sys.setrecursionlimit(1000000)

  def end(self):
    pass

  def QSHTTLABDLMM(self, node, depth, alpha, beta, starttime, maxtime, qslimit):
    #Build children with history table values
    children = {}
    moves = []
   
    if time.time() - starttime >= maxtime:
      return None
    for all in node.getChildren():
      if all in self.historytable:
        children[all] = self.histortytable[all]
      else:
        children[all] = 0

    #Sort them based on those values
    sortedchildren = sorted(children.iteritems(), key=operator.itemgetter(1), reverse=True)
    children = dict(sortedchildren)

    for each in children:
      #Check if the time has run out
      if time.time() - starttime >= maxtime:
        return None
      newvalue = self.QSHTABMinV(each, depth - 1, alpha, beta, starttime, maxtime, qslimit, qslimit)
      if newvalue == None:
        return None
      elif newvalue >= alpha and newvalue < beta:
        if newvalue > alpha:
          moves = []
        moves.append(ValToChild(newvalue, each))
        alpha = newvalue
        if each in self.historytable:
          self.historytable[each] += 1
        else:
          self.historytable[each] = 1
      elif newvalue >= beta:
        if each in self.historytable:
          self.historytable[each] += 1
        else:
          self.historytable[each] = 1
        break

    randommove = random.randint(0, len(moves) - 1)
    return moves[randommove].child.movethatgotmehere
  
  def QSHTABMinV(self, node, depth, alpha, beta, starttime, maxtime, qslimit, qsdepth):
    #Out of Time
    if time.time() - starttime >= maxtime:
      return None
    
    #Get Heuristic value, Depth Limit Reached
    if depth == 0:
      if node.player == 1 and node.quiescenceHeuristicValue() and qsdepth > 0:
        return node.heuristicValue()
      elif node.player == 0 and node.quiescenceHeuristicValue() and qsdepth > 0:
        return node.heuristicValue()


    #Create sorted dictionary of children based on history table value
    children = {}
    for all in node.getChildren():
      if all in self.historytable:
        children[all] = self.historytable[all]
      else:
        children[all] = 0
    sortedchildren = sorted(children.iteritems(), key=operator.itemgetter(1), reverse=True)
    children = dict(sortedchildren)
    #Checkmate or stalemate due to 0 moves
    if len(children) == 0:
      if node in self.historytable:
        self.historytable[node] += 1
      else:
        self.historytable[node] = 1
      #Checkmate For this player
      if node.kingInCheck(1, 1, 1, 1):
        return sys.maxint * -1
      #Checkmate For the other player
      elif node.kingInCheck(1, 1, 1, 1, True):
        return sys.maxint
      #Stalemate
      else:
        return 0
    
    if time.time() - starttime >= maxtime:
      return None

    #Stalemate via 3 repeated board states
    if node.parent is not None:
      pmove = node.parent.movethatgotmehere
      cmove = node.movethatgotmehere
      if node.parent.parent is not None:
        ppmove = node.parent.parent.movethatgotmehere
        if cmove is not None and ppmove is not None and cmove[0] == ppmove[2] and cmove[1] == ppmove[3]:
          if node.parent.parent.parent is not None:
            pppmove = node.parent.parent.parent.movethatgotmehere
            if pmove is not None and pppmove is not None and pmove[0] == pppmove[2] and pmove[1] == pppmove[3]:
              if node.parent.parent.parent.parent is not None:
                ppppmove = node.parent.parent.parent.parent.movethatgotmehere
                if ppmove is not None and ppppmove is not None and ppmove[0] == ppppmove[2] and ppmove[1] == ppppmove[3]:
                  if node.parent.parent.parent.parent.parent is not None:
                    pppppmove = node.parent.parent.parent.parent.parent.movethatgotmehere
                    if pppmove is not None and pppppmove is not None and pppmove[0] == pppppmove[2] and pppmove[1] == pppppmove[3]:
                      if node in self.historytable:
                        self.historytable[node] += 1
                      else:
                        self.historytable[node] = 1
                      return 0

    
    flattenedboard = [item for sublist in node.board for item in sublist]
    
    #2 kings stalemate
    if flattenedboard.count('.') == 62:
      if node in self.historytable:
        self.historytable[node] += 1
      else:
        self.historytable[node] = 1
      return 0

    if flattenedboard.count('.') == 61:
      if flattenedboard.count('b') == 1 or flattenedboard.count('n') == 1 or \
         flattenedboard.count('B') == 1 or flattenedboard.count('N') == 1:
        if node in self.historytable:
          self.historytable[node] += 1
        else:
          self.historytable[node] = 1
        return 0
    
    if flattenedboard.count('.') == 60:
      if flattenedboard.count('b') == 1 and flattenedboard.count('B') == 1:
        if flattenedboard.index('b')%8 == flattenedboard.index('B')%8 and \
           int(len(flattenedboard) / flattenedboard.index('b'))%2 == \
           int(len(flattenedboard) / flattenedboard.index('B'))%2:
          if node in self.historytable:
            self.historytable[node] += 1
          else:
            self.historytable[node] = 1
          return 0

    if node.turnstostalemate == 0:
      if node in self.historytable:
        self.historytable[node] += 1
      else:
        self.historytable[node] = 1
      return 0
        
    for each in children:
      #Check if the time has run out
      if time.time() - starttime >= maxtime:
        return None
      if depth == 0 and qsdepth > 0:
        newvalue = self.QSHTABMaxV(each, depth, alpha, beta, starttime, maxtime, qslimit, qsdepth - 1)
      else:
        newvalue = self.QSHTABMaxV(each, depth-1, alpha, beta, starttime, maxtime, qslimit, qslimit)
      if newvalue == None:
        return None

      elif newvalue > alpha and newvalue < beta:
        beta = newvalue
        if each in self.historytable:
          self.historytable[each] += 1
        else:
          self.historytable[each] = 1
      elif newvalue <= alpha:
        if each in self.historytable:
          self.historytable[each] += 1
        else:
          self.historytable[each] = 1
        break

    return beta

  
  def QSHTABMaxV(self, node, depth, alpha, beta, starttime, maxtime, qslimit, qsdepth):
    #Out of Time
    if time.time() - starttime >= maxtime:
      return None
    
    #Get Heuristic value, Depth Limit Reached
    if depth == 0:
      if node.player == 1 and node.quiescenceHeuristicValue() and qsdepth > 0:
        return node.heuristicValue()
      elif node.player == 0 and node.quiescenceHeuristicValue() and qsdepth > 0:
        return node.heuristicValue()

    #Create sorted dictionary of children based on history table value
    children = {}
    for all in node.getChildren():
      if all in self.historytable:
        children[all] = self.historytable[all]
      else:
        children[all] = 0
    
    sortedchildren = sorted(children.iteritems(), key=operator.itemgetter(1), reverse=True)
    children = dict(sortedchildren)
      
    #Checkmate or stalemate due to 0 moves
    if len(children) == 0:
      if node in self.historytable:
        self.historytable[node] += 1
      else:
        self.historytable[node] = 1
      #Checkmate For this player
      if node.kingInCheck(1, 1, 1, 1):
        return sys.maxint * -1
      #Checkmate For the other player
      elif node.kingInCheck(1, 1, 1, 1, True):
        return sys.maxint
      #Stalemate
      else:
        return 0
    
    if time.time() - starttime >= maxtime:
      return None

    #Stalemate via 3 repeated board states
    if node.parent is not None:
      pmove = node.parent.movethatgotmehere
      cmove = node.movethatgotmehere
      if node.parent.parent is not None:
        ppmove = node.parent.parent.movethatgotmehere
        if cmove is not None and ppmove is not None and cmove[0] == ppmove[2] and cmove[1] == ppmove[3]:
          if node.parent.parent.parent is not None:
            pppmove = node.parent.parent.parent.movethatgotmehere
            if pmove is not None and pppmove is not None and pmove[0] == pppmove[2] and pmove[1] == pppmove[3]:
              if node.parent.parent.parent.parent is not None:
                ppppmove = node.parent.parent.parent.parent.movethatgotmehere
                if ppmove is not None and ppppmove is not None and ppmove[0] == ppppmove[2] and ppmove[1] == ppppmove[3]:
                  if node.parent.parent.parent.parent.parent is not None:
                    pppppmove = node.parent.parent.parent.parent.parent.movethatgotmehere
                    if pppmove is not None and pppppmove is not None and pppmove[0] == pppppmove[2] and pppmove[1] == pppppmove[3]:
                      if node in self.historytable:
                        self.historytable[node] += 1
                      else:
                        self.historytable[node] = 1
                      return 0

    
    flattenedboard = [item for sublist in node.board for item in sublist]
    
    #2 kings stalemate
    if flattenedboard.count('.') == 62:
      if node in self.historytable:
        self.historytable[node] += 1
      else:
        self.historytable[node] = 1
      return 0

    if flattenedboard.count('.') == 61:
      if flattenedboard.count('b') == 1 or flattenedboard.count('n') == 1 or \
         flattenedboard.count('B') == 1 or flattenedboard.count('N') == 1:
        if node in self.historytable:
          self.historytable[node] += 1
        else:
          self.historytable[node] = 1
        return 0
    
    if flattenedboard.count('.') == 60:
      if flattenedboard.count('b') == 1 and flattenedboard.count('B') == 1:
        if flattenedboard.index('b')%8 == flattenedboard.index('B')%8 and \
           int(len(flattenedboard) / flattenedboard.index('b'))%2 == \
           int(len(flattenedboard) / flattenedboard.index('B'))%2:
          if node in self.historytable:
            self.historytable[node] += 1
          else:
            self.historytable[node] = 1
          return 0

    if node.turnstostalemate == 0:
      if node in self.historytable:
        self.historytable[node] += 1
      else:
        self.historytable[node] = 1
      return 0
        
    for each in children:
      #Check if the time has run out
      if time.time() - starttime >= maxtime:
        return None
      if depth == 0 and qsdepth > 0:
        newvalue = self.QSHTABMinV(each, depth, alpha, beta, starttime, maxtime, qslimit, qsdepth - 1)
      else:
        newvalue = self.QSHTABMinV(each, depth-1, alpha, beta, starttime, maxtime, qslimit, qslimit)

      if newvalue == None:
        return None

      elif newvalue > alpha and newvalue < beta:
        alpha = newvalue
        if each in self.historytable:
          self.historytable[each] += 1
        else:
          self.historytable[each] = 1
      elif newvalue >= beta:
        if each in self.historytable:
          self.historytable[each] += 1
        else:
          self.historytable[each] = 1
        break
    return alpha

  def run(self):
    node = self.buildRootNode()
    #Clear the history table for each new turn
    self.historytable = {}
    #QSHTTLABIDDLMM, because this is where the iterativeness happens and time is started
    #Time heuristic will probably fail at being a good heuristic, but sometimes not.
    #But hey, it exists right?
    #QS Limit is set to 3 for now.
    starttime = time.time()
    maxtime = self.timeHeuristic(self.turnNumber())
    move = None
    for a in range(1, 100):
      newmove = self.QSHTTLABDLMM(node, a, -sys.maxint, sys.maxint, starttime, maxtime, 3)
      if newmove != None:
        move = newmove
      else:
        break
    print chr(ord('a') + move[1]) + str(move[0] * -1 + 8) + ' ' + chr(ord('a') + move[3]) + str(move[2] * -1 + 8)
    
    #Converts my data into data the server knows about
    for a in self.pieces:
      if move[0] * -1 + 8 == a.getRank() and move[1] + 1 == a.getFile():
        if len(move) == 4:
          a.move(move[3] + 1, move[2] * -1 + 8, 0)
        elif len(move) == 5:
          a.move(move[3] + 1, move[2] * -1 + 8, move[4])
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
