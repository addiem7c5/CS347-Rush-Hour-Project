# File: node.py
# Author: Addie Martin
from board import Board

class Node:
# Class: Node
# Description: This class ties a Rush Hour puzzle state to
#	       the action taken to get to it from its parent
#              state. It also holds its parent state (if one exists)
#              and it's children states. This is used for Breadth
#              First Search algorithm.

	def __init__(self, board, action, depth, h):
	# Function: __init__
	# Paramaters: The Instance of Node, A board(state) to add to the node
	#             and, an action to add to the node in the style of:
	#              [[Display character, [Coordinates occupied], Whether or not
	#                it's the escape car, the vehicle's orientation], and the
	#				 direction the car can go]
        #             and the Node's depth on the tree.
	# Description: Initializes a new Node object, sets its parent initally to
	#              none, and children to an empty list.
		self.state = board
		self.actiontocurrent = action
		self.parent = None
		self.children = []
		self.depth = depth
		self.hvalue = h
	
	def __eq__(self, b):
	# Function: __eq__
	# Parameters: The Instance of Node, and another Node
	# Description: Takes another node, and sees if its state is
	#              equal to the state 
	# Returns: 1 if the states are equal, 0 if not
		if self.state == b.state:
			return 1
		else:
			return 0
	def __cmp__(self, b):
		if self.state == b.state:
			return 0
		else:
			return 1
	def __lt__(self, other):
		return self.depth + self.hvalue < other.depth + other.hvalue

	def __gt__(self, other):
		return self.depth + self.state.hvalue() > other.depth + \
						     other.state.hvalue()

	def __hash__(self):
		outstr = ""
		for y in self.state.spaces:
			for x in y:
				outstr += x
		return hash(outstr)

	def getStateBoardStringForHash(self):
		outstr = ""
		for y in self.state.spaces:
			for x in y:
				outstr += x
		return outstr		
	
	def setParent(self, node):
	# Function: setParent
	# Parameters: The Instance of the Node, and another Node
	# Description: Takes another node, and sets this nodes parent 
	#              to it.
		self.parent = node
	
	def addChild(self, node):
	# Function: addChild
	# Parameters: The Instance of the Node, and another Node
	# Description: Takes another node, and adds it to this nodes 
	#              children list.
		self.children.append(node)
