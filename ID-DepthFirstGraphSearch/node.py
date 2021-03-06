# File: node.py
# Author: Addie Martin
from board import Board

class Node:
# Class: Node
# Description: This class ties a Rush Hour puzzle state to
#			   the action taken to get to it from its parent
#              state. It also holds its parent state (if one exists)
#              and it's children states. This is used for Breadth
#              First Search algorithm.

	def __init__(self, board, action, depth):
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
	
	def __eq__(self, b):
	# Function: __eq__
	# Parameters: The Instance of Node, and another Node
	# Description: Takes another node, and sees if its state and depth are
	#              equal to the state and depth of this Instance.
	# Returns: 1 if the states are equal, 0 if not
		if self.state == b.state and self.depth == b.depth:
			return 1
		else:
			return 0
	
	def getStateBoardStringForHash(self):
		outstr = ""
		for y in self.state.spaces:
			for x in y:
				outstr += x
		outstr+=str(self.depth)
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
