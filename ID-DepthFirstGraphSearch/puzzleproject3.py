# File: puzzleproject2.py
# Author: Addie Martin
import random
import sys
import time
from collections import deque
from board import Board
from node import Node
moves = 0
boardname = ""
current = Board()
#Loading in the board
if len(sys.argv) <= 1:
	boardname = raw_input("What board would you like to load?\t")
else:
	boardname = sys.argv[1]
if current.loadBoard(boardname) == 0:
	print boardname, "does not exist!"
else:
	#Do the ID-DFGS Algorithm
	print "We are going to do an optimal Iterative Deepening", 
        print "Depth First Graph Search on", boardname
	current.printDisplay()
	elapsedtime = time.time()
	stackofmoves = []
	iterationlevel = 0

	#Initial Node
	n = Node(current, None, 0)
	stackofmoves.append(n)
	closedlist = set()
	closedlist.add(n.getStateBoardStringForHash())
	#for a in closedlist:
	#	print a
	#Search for a win at the beginning of the frontier
	while not stackofmoves[-1].state.isAWin():
		                    			
		s = stackofmoves[-1]
		
		stackofmoves.pop()
		#See if the current nodes depth is less than the iteration level
		#If it is, we can still expand
		if s.depth < iterationlevel:
			for a in s.state.whatCanMove():
				n = Node(s.state.doAction(a), a, s.depth + 1)
				#Check if the boards string rep is in the closed list
									
				if n.getStateBoardStringForHash() not in closedlist:
					n.setParent(s)
					s.addChild(n)
					stackofmoves.append(n)
					closedlist.add(n.getStateBoardStringForHash())
		
		if len(stackofmoves) == 0:
			s = []
			stackofmoves = []
			n = Node(current, None, 0)
			closedlist = set()
			closedlist.add(n.getStateBoardStringForHash())
			stackofmoves.append(n)
			iterationlevel += 1
	elapsedtime = time.time() - elapsedtime
	#Prepare and output moves
	endmoves = [stackofmoves[-1]]
	currentnode = stackofmoves[-1]
	while currentnode.parent is not None:
		moves = moves + 1
		endmoves.append(currentnode.parent)
		currentnode = currentnode.parent
	print "The time it took for ID-DFGS is", elapsedtime, "seconds."
	print "The AI won, in", moves, "moves!"
	raw_input("Press enter to see the moves taken!")
	endmoves.pop()
	while len(endmoves) > 0:
		a = endmoves[-1].actiontocurrent
		endmoves[-1].state.printDisplay()
		endmoves.pop().state.printAction(a)

