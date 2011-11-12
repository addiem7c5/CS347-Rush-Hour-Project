# File: puzzleproject4.py
# Author: Addie Martin
import random
import sys
import time
from board import Board
from node import Node


def HValueFromDistanceToExit(n):
	for a in n.spaces:
		if a.count('?') > 0:
			return len(a) - a.index('?')

def HValueFromDistanceToExitNegative(n):
	return (-1 * HValueFromDistanceToExit(n))

def HValueFromDistanceAndNumCars(n):
	numcars = 0
	for a in n.spaces:
		if a.count('?') > 0:
			for b in a:
				if b != '.' and b != '?':
					numcars+=1
	return HValueFromDistanceToExit(n) + numcars 
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

	#Do the A* Algorithm
	print "We are going to do an A* Search on", boardname 
	current.printDisplay()
	elapsedtime = time.time()
	pqueue = []
	pqueue.append(Node(current, None, 0, HValueFromDistanceAndNumCars(current)))
	closedset = dict()
	#Search for a win at the beginning of the frontier
	while not pqueue[0].state.isAWin():
		currentnode = pqueue.pop(0)
		closedset[currentnode] = currentnode.depth
		for a in currentnode.state.whatCanMove():
			newstate = currentnode.state.doAction(a)
			newnode = Node(newstate, a, currentnode.depth + 1, \
				       HValueFromDistanceAndNumCars(newstate))
			if newnode not in closedset:
				newnode.setParent(currentnode)
				pqueue.append(newnode)
				closedset[newnode] = newnode.depth
			elif newnode in closedset and newnode.depth < closedset[newnode] :
				if newnode in pqueue:
					pqueue[pqueue.index(newnode)].depth = newnode.depth
					pqueue[pqueue.index(newnode)].setParent(currentnode)
				else:
					newnode.setParent(currentnode)
					pqueue.append(newnode)
					closedset[newnode] = newnode.depth
		pqueue.sort()
	elapsedtime = time.time() - elapsedtime
	#Prepare and output moves
	


	winmoves = []
	cnode = pqueue[0]
	while cnode.parent is not None:
		winmoves.append(cnode.actiontocurrent)
		cnode = cnode.parent
	print "The time it took for A* is", elapsedtime, "seconds."
	print "The AI won, in", len(winmoves), "moves!"
	raw_input("Press enter to see the moves taken!")
	
	while len(winmoves) > 0:
		cnode.state.printAction(winmoves.pop())
