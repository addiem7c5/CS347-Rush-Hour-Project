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

	def __init__(self, board, action):
	# Function: __init__
	# Paramaters: The Instance of Node, A board(state) to add to the node
	#             and, an action to add to the node in the style of:
	#              [[Display character, [Coordinates occupied], Whether or not
	#                it's the escape car, the vehicle's orientation], and the
	#				 direction the car can go]
	# Description: Initializes a new Node object, sets its parent initally to
	#              none, and children to an empty list.
		self.state = board
		self.actiontocurrent = action
		self.parent = None
		self.children = []
	
	def __eq__(self, b):
	# Function: __eq__
	# Parameters: The Instance of Node, and another Node
	# Description: Takes another node, and sees if its state is equal to the
	#              state of this Instance.
	# Returns: 1 if the states are equal, 0 if not
		if self.state == b.state:
			return 1
		else:
			return 0
	
	def getStateBoardStringForHash(self):
		str = ""
		for y in self.state.spaces:
			for x in y:
				str += x
		return str			
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
	
