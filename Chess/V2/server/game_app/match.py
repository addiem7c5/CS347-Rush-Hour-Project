# -*- coding: iso-8859-1 -*-
from base import *
from matchUtils import *
from objects import *
import networking.config.config
from collections import defaultdict
from networking.sexpr.sexpr import *
import os
import itertools
import scribe
from copy import deepcopy

Scribe = scribe.Scribe

def loadClassDefaults(cfgFile = "config/defaults.cfg"):
  cfg = networking.config.config.readConfig(cfgFile)
  for className in cfg.keys():
    for attr in cfg[className]:
      setattr(eval(className), attr, cfg[className][attr])

class Match(DefaultGameWorld):
  def __init__(self, id, controller, cfgFile="config/initBoardState.txt"):
    self.id = int(id)
    self.controller = controller
    DefaultGameWorld.__init__(self)
    self.scribe = Scribe(self.logPath())
    self.addPlayer(self.scribe, "spectator")
    self.cfgFile = cfgFile

    #TODO: INITIALIZE THESE!
    self.moves = 0
    self.turnNumber = 0
    self.playerID = 0
    self.gameNumber = id 
    self.TurnsToStalemate = 100
    self.timeInc = 1
    self.player0Time = 90000
    self.player1Time = 90000 #15 minutes in centiseconds

  def addPlayer(self, connection, type="player"):
    connection.type = type
    if len(self.players) >= 2 and type == "player":
      return "Game is full"
    if type == "player":
      self.players.append(connection)
    elif type == "spectator":
      self.spectators.append(connection)
      #If the game has already started, send them the ident message
      if (self.turn is not None):
        self.sendIdent([connection])
    return True

  def removePlayer(self, connection):
    if connection in self.players:
      if self.turn is not None:
        winner = self.players[1 - self.getPlayerIndex(connection)]
        self.declareWinner(winner,"Opponent Dropped")
      self.players.remove(connection)
    else:
      self.spectators.remove(connection)

  def start(self):
    if len(self.players) < 2:
      return "Game is not full"
    if self.winner is not None or self.turn is not None:
      return "Game has already begun"
    
    #TODO: START STUFF
    board = file(self.cfgFile, 'r').read() #reads in the initial board state
    assert (len(board) >= 64 )

    self.turnNumber = -1
    self.turn = 0
    #Creates all of the pieces
    curRank = 0
    curFile = 1
    for square in board:
      if square == '\n':
        curFile = 1
        curRank += 1
      if square == 'R':
        self.addObject(Piece(self, self.nextid, 1, curFile, 8-curRank, 0, ord('R')))
        self.nextid += 1
        curFile += 1
      if square == 'N':
        self.addObject(Piece(self, self.nextid, 1, curFile, 8-curRank, 0, ord('N')))
        self.nextid += 1
        curFile += 1
      if square == 'B':
        self.addObject(Piece(self, self.nextid, 1, curFile, 8-curRank, 0, ord('B')))
        self.nextid += 1
        curFile += 1
      if square == 'K':
        self.addObject(Piece(self, self.nextid, 1, curFile, 8-curRank, 0, ord('K')))
        self.nextid += 1
        curFile += 1
      if square == 'Q':
        self.addObject(Piece(self, self.nextid, 1, curFile, 8-curRank, 0, ord('Q')))
        self.nextid += 1
        curFile += 1
      if square == 'P':
        self.addObject(Piece(self, self.nextid, 1, curFile, 8-curRank, 0, ord('P')))
        self.nextid += 1
        curFile += 1
      if square == 'r':
        self.addObject(Piece(self, self.nextid, 0, curFile, 8-curRank, 0, ord('R')))
        self.nextid += 1
        curFile += 1
      if square == 'n':
        self.addObject(Piece(self, self.nextid, 0, curFile, 8-curRank, 0, ord('N')))
        self.nextid += 1
        curFile += 1
      if square == 'b':
        self.addObject(Piece(self, self.nextid, 0, curFile, 8-curRank, 0, ord('B')))
        self.nextid += 1
        curFile += 1
      if square == 'k':
        self.addObject(Piece(self, self.nextid, 0, curFile, 8-curRank, 0, ord('K')))
        self.nextid += 1
        curFile += 1
      if square == 'q':
        self.addObject(Piece(self, self.nextid, 0, curFile, 8-curRank, 0, ord('Q')))
        self.nextid += 1
        curFile += 1
      if square == 'p':
        self.addObject(Piece(self, self.nextid, 0, curFile, 8-curRank, 0, ord('P')))
        self.nextid += 1
        curFile += 1
      if square == '.':
        curFile += 1
    self.turn = self.players[1]
    self.nextTurn()
    return True


  def nextTurn(self):
    self.turnNumber += 1
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 1
    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 0

    else:
      return "Game is over."

    for obj in self.objects.values():
      obj.nextTurn()


    self.checkWinner()
    self.moves = 1
    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)
    self.animations = ["animations"]
    return True

  def checkWinner(self):
    #TODO: Make this check if a player won, and call declareWinner with a player if they did, illegal move defaulting is handled at the end of the piece move function
    #if they didn't make a move, they lose
    if self.moves is not 0:
      message = ""
      if self.playerID is 0:
        message += "Black "
      else:
        message += "White "
      message += "failed to make a move!"
      self.declareWinner(self.players[self.playerID],message)
    if self.TurnsToStalemate == 0:
      self.declareDraw("100 moves without a capture or pawn advancement, Stalemate!")
    if len( [ i for i in self.objects.values() if isinstance(i, Piece)] ) == 2:
      self.declareDraw("Only Kings Left, Stalemate!")
    if len( [ i for i in self.objects.values() if isinstance(i, Piece)] ) == 3:
      for p in self.objects.values():
        if isinstance(p,Piece):
          if p.type == ord('B'):
            self.declareDraw("With a King Vs a King and a Bishop it is impossible to checkmate, Stalemate!")
          if p.type == ord('N'):
            self.declareDraw("With a King Vs a King and a Knight it is impossible to checkmate, Stalemate!")
    stalemate = True
    bColor = -1
    for i in self.objects.values():
      if isinstance(i,Piece):
        if i.type is not ord('K') and i.type is not ord('B'):
          stalemate = False
          break
        if i.type is ord('B'):
          if bColor is -1:
            bColor = (i.rank+i.file)%2
          else:
            if (i.rank+i.file)%2 is not bColor:
              stalemate = False
              break
    if stalemate is True:
      self.declareDraw("With only Kings and Bishops, with all of the Bishops on the same color, Checkmate is impossible, Stalemate!")
    moveList = []
    moveList.append( sorted([i.toList() for i in self.objects.values() if i.__class__ is Move], reverse = True))
    #print "Debugging info: " + `len(moveList[0])`+ ", " + `self.TurnsToStalemate` + `moveList`
    if len(moveList[0]) >= 8 and self.TurnsToStalemate <= 92:
      trippleRepeat = True
      for i in [0,1,4,5]:
        #print "Past Move " +`i`+": (" + `moveList[i][1]` + "," + `moveList[i][2]` + ") to (" + `moveList[i][3]` +"," + `moveList[i][4]` + ")"
        if not (moveList[0][i][3] is moveList[0][i+2][1] and moveList[0][i][4] is moveList[0][i+2][2] and moveList[0][i][1] is moveList[0][i+2][3] and moveList[0][i][2] is moveList[0][i+2][4]):
          trippleRepeat = False
      if trippleRepeat:
        self.declareDraw("Board state repeated three times in a row, Stalemate Declared!")

    pass
  
  def declareDraw(self, reason=''):
    self.winner = 'No one.'
    
    msg = ["game-winner", self.id, 'No one.', 2, reason]
    
    self.scribe.writeSExpr(msg)
    self.scribe.finalize()
    self.removePlayer(self.scribe)

    for p in self.players + self.spectators:
      p.writeSExpr(msg)

    self.sendStatus([self.turn])
    self.playerID ^= 1
    self.sendStatus([self.players[self.playerID]])
    self.playerID ^= 1
    self.turn = None

  def declareWinner(self, winner, reason=''):
    self.winner = winner

    msg = ["game-winner", self.id, self.winner.user, self.getPlayerIndex(self.winner), reason]
    self.scribe.writeSExpr(msg)
    self.scribe.finalize()
    self.removePlayer(self.scribe)

    for p in self.players + self.spectators:
      p.writeSExpr(msg)

    self.sendStatus([self.turn])
    self.playerID ^= 1
    self.sendStatus([self.players[self.playerID]])
    self.playerID ^= 1
    self.turn = None
    
  def logPath(self):
    return "logs/" + str(self.id) + ".gamelog"

  @derefArgs(Piece, None, None, None)
  def move(self, object, file, rank, type):
    return object.move(file, rank, type, )


  def sendIdent(self, players):
    if len(self.players) < 2:
      return False
    list = []
    for i in itertools.chain(self.players, self.spectators):
      list += [[self.getPlayerIndex(i), i.user, i.screenName, i.type]]
    for i in players:
      i.writeSExpr(['ident', list, self.id, self.getPlayerIndex(i)])

  def getPlayerIndex(self, player):
    try:
      playerIndex = self.players.index(player)
    except ValueError:
      playerIndex = -1
    return playerIndex

  def sendStatus(self, players):
    for i in players:
      i.writeSExpr(self.status())
      i.writeSExpr(self.animations)
    return True


  def status(self):
    msg = ["status"]

    msg.append(["game", self.turnNumber, self.playerID, self.gameNumber, self.TurnsToStalemate, self.player0Time, self.player1Time])

    typeLists = []
    typeLists.append(["Move"] + sorted([i.toList() for i in self.objects.values() if i.__class__ is Move], reverse = True))
    
    typeLists.append(["Piece"] + [i.toList() for i in self.objects.values() if i.__class__ is Piece])

    msg.extend(typeLists)

    return msg

  #checks if a  player is in check
  def inCheck(self,owner):
    temp = self.playerID
    temp2 = self.moves
    self.playerID = owner^1
    self.moves = 1
    king = [ i for i in self.objects.values() if isinstance(i, Piece) and i.type is ord('K') and i.owner is owner][0]
    #print "Checking for Check!, King at Rank " + `king.rank` + " File " + `king.file`
    for i in self.objects.values():
      if isinstance(i,Piece) and i.owner is not owner:
        vMoveReturn = i.verifyMove(king.file,king.rank,ord('Q')) 
        # Kenneth Perry : if the file and rank are bad, why are you checking?
        if vMoveReturn == True and i.file != -1 and i.rank != -1:
          #print "Check! " + "Rank " + `i.rank` + " File " + `i.file`
          self.playerID = temp
          self.moves = temp2
          return True
        #else:
          #print vMoveReturn + " (" + chr(i.type) + " at " + `i.file`+ ","+ `i.rank`
    self.playerID = temp
    self.moves = temp2
    return False

  def noLegalMoves(self,owner):
    newGameState = deepcopy(self)
    newGameState.playerID = owner
    #print "Checking for a lack of legal moves!"
    for p in newGameState.objects.values():
      #print "There exist things in newGameState.objects"
      if isinstance(p,Piece) and p.owner is owner:
        for i in range(1,9):
          for j in range(1,9):
           # print "Checking  Rank " + `p.rank` + " to " + `i` + " File " + `p.file` + " to " + `j`
    
            if p.makeMove(j,i,ord('Q')) is True:
              #print "Get Out Of Check solution found!" + chr(p.type) + " at Rank " + `p.rank` + " to " + `i` + " File " + `p.file` + " to " + `j`
              return False
    #if no possible move gets out of check, then they are in checkmate
    return True

loadClassDefaults()

