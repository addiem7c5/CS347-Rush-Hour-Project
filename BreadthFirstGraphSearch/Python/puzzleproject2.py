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
	#Do the BFGS Algorithm
	print "We are going to do Breadth First Graph Search on", boardname
	current.printDisplay()
	elapsedtime = time.time()
	queueofmoves = deque()
	checklisttime = 0
	#Initial Node
	n = Node(current, None)
	queueofmoves.append(n)
	closedlist = set(n.getStateBoardStringForHash())
	#Search for a win at the beginning of the frontier
	while not queueofmoves[0].state.isAWin():
		print "Frontier: ", len(queueofmoves)
		print "Closed: ", len(closedlist)
		q = queueofmoves[0]
		queueofmoves.popleft()
		for a in q.state.whatCanMove():
			n = Node(q.state.doAction(a), a)
			#Check if the boards string rep is in the closed list
			if n.getStateBoardStringForHash() not in closedlist:
				n.setParent(q)
				q.addChild(n)
				queueofmoves.append(n)
				closedlist.add(n.getStateBoardStringForHash())
	elapsedtime = time.time() - elapsedtime
	#Prepare and output moves
	endmoves = [queueofmoves[0]]
	currentnode = queueofmoves[0]
	while currentnode.parent is not None:
		moves = moves + 1
		endmoves.append(currentnode.parent)
		currentnode = currentnode.parent
	print "The time it took for BFGS is", elapsedtime, "seconds."
	print "The AI won, in", moves, "moves!"
	raw_input("Press enter to see the moves taken!")
	endmoves.pop()
	while len(endmoves) > 0:
		a = endmoves[-1].actiontocurrent
		endmoves.pop().state.printAction(a)

