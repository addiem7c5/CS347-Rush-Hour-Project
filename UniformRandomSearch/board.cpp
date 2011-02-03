/*  File: board.cpp
    Author: Addie Martin
    This is the class definition file for the Board class. All functions
    from this class are defined here.
*/
#include <fstream>
#include <iostream>
#include <list>
#include <algorithm>
#include "board.h"

/*
    Function: Board Default Constructor
    Description: Empty default constructor.
    Parameters: None
    Returns: Nothing
*/ 
Board::Board()
{
}

/*
    Function: Board Copy Constructor
    Description: Copies one board into this board
    Parameters: Const Reference to a board
    Returns: Nothing
*/ 
Board::Board(const Board& b) : m_spaces(b.m_spaces)
{
}

/*
    Function: canMove
    Description: Takes a vehicle and sees if it can move
		 in the current board.
    Parameters: Pointer to a Vehicle
    Returns: A vector of all possible moves this vehicle
	     can make.
*/ 
vector<short> Board::canMove(Vehicle *v)
{
	vector<short> possible;
	possible.push_back(0);
	if(v->getOrientation() == RIGHTLEFT)
	{
		if((v->getOccupying()[0].x + 1 < m_spaces[v->getOccupying()[0].y].size() &&
		   (m_spaces[v->getOccupying()[0].y][v->getOccupying()[0].x + 1] == '.' ||
		   (m_spaces[v->getOccupying()[0].y][v->getOccupying()[0].x + 1] == '-' && v->getDisplay() == '?'))) || 
		   (v->getOccupying()[1].x + 1 < m_spaces[v->getOccupying()[1].y].size() &&
		   (m_spaces[v->getOccupying()[1].y][v->getOccupying()[1].x + 1] == '.' ||
		   (m_spaces[v->getOccupying()[1].y][v->getOccupying()[1].x + 1] == '-' && v->getDisplay() == '?'))) ||
		   (v->getSize() > 2 && 
		    v->getOccupying()[2].x + 1 < m_spaces[v->getOccupying()[2].y].size() &&
		   (m_spaces[v->getOccupying()[2].y][v->getOccupying()[2].x + 1] == '.' ||
		   (m_spaces[v->getOccupying()[2].y][v->getOccupying()[2].x + 1] == '-' && v->getDisplay() == '?'))))
		{
			possible.push_back(1);
		}
		else if((v->getOccupying()[0].x - 1  >= 0 &&
		        (m_spaces[v->getOccupying()[0].y][v->getOccupying()[0].x - 1] == '.' ||
		        (m_spaces[v->getOccupying()[0].y][v->getOccupying()[0].x - 1] == '-' && v->getDisplay() == '?'))) || 
		        (v->getOccupying()[1].x - 1 >= 0 &&
		        (m_spaces[v->getOccupying()[1].y][v->getOccupying()[1].x - 1] == '.' ||
		        (m_spaces[v->getOccupying()[1].y][v->getOccupying()[1].x - 1] == '-' && v->getDisplay() == '?'))) ||
		        (v->getSize() > 2 && 
		         v->getOccupying()[2].x - 1 >= 0 &&
		        (m_spaces[v->getOccupying()[2].y][v->getOccupying()[2].x - 1] == '.' ||
		        (m_spaces[v->getOccupying()[2].y][v->getOccupying()[2].x - 1] == '-' && v->getDisplay() == '?'))))
		{
			possible.push_back(-1);
		}
	}
	else
	{
		if((v->getOccupying()[0].y + 1 < m_spaces.size() &&
		   (m_spaces[v->getOccupying()[0].y + 1][v->getOccupying()[0].x] == '.' ||

/*
    Function: Board Constructor
    Description: Empty default constructor.
    Parameters: None
    Returns: Nothing
*/ 		   (m_spaces[v->getOccupying()[0].y + 1][v->getOccupying()[0].x] == '-' && v->getDisplay() == '?'))) || 
		   (v->getOccupying()[1].y + 1 < m_spaces.size() &&
		   (m_spaces[v->getOccupying()[1].y + 1][v->getOccupying()[1].x] == '.' ||
		   (m_spaces[v->getOccupying()[1].y + 1][v->getOccupying()[1].x] == '-' && v->getDisplay() == '?'))) ||
		   (v->getSize() > 2 && 
		    v->getOccupying()[2].y + 1 < m_spaces.size() &&
		   (m_spaces[v->getOccupying()[2].y + 1][v->getOccupying()[2].x] == '.' ||
		   (m_spaces[v->getOccupying()[2].y + 1][v->getOccupying()[2].x] == '-' && v->getDisplay() == '?'))))
		{
			possible.push_back(1);
		}
		else if((v->getOccupying()[0].y - 1 >= 0 &&
		        (m_spaces[v->getOccupying()[0].y - 1][v->getOccupying()[0].x] == '.' ||
		        (m_spaces[v->getOccupying()[0].y - 1][v->getOccupying()[0].x] == '-' && v->getDisplay() == '?'))) || 
		        (v->getOccupying()[1].y - 1 >= 0 &&
		        (m_spaces[v->getOccupying()[1].y - 1][v->getOccupying()[1].x] == '.' ||
			(m_spaces[v->getOccupying()[1].y - 1][v->getOccupying()[1].x] == '-' && v->getDisplay() == '?'))) ||
		        (v->getSize() > 2 && 
		         v->getOccupying()[2].y - 1 >= 0 &&
		        (m_spaces[v->getOccupying()[2].y - 1][v->getOccupying()[2].x] == '.' ||
		        (m_spaces[v->getOccupying()[2].y - 1][v->getOccupying()[2].x] == '-' && v->getDisplay() == '?'))))
		{
			possible.push_back(-1);
		}
	}
	return possible;
}


/*
    Function: loadBoard
    Description: Takes a string that is a filename, and loads a Rush Hour board
		 into memory.
    Parameters: string 
    Returns: true if successful, false if unsuccessful
*/ 
bool Board::loadBoard(string filename)
{
	ifstream infile(filename.c_str());
	string instring;
	string total = "";
	int size;
	vector<char> currentrow;
	bool addeddash = false;
	if(infile.is_open() == false)
	{	
		return false;
	}
	else
	{
		infile>>size;
		while(!infile.eof())
		{
			infile>>instring;
			total += instring;
		}
		infile.close();
		
		for(int i=0; i<size; i++)
		{
			for(int j=0; j<size; j++)
			{
				if(addeddash)
					currentrow.push_back(total[i*size + j + 1]);
				else
					currentrow.push_back(total[i*size + j]);
				if(total[i*size + j + 1] == '-')
				{
					currentrow.push_back('-');
					addeddash = true;
				}
			}
			m_spaces.push_back(currentrow);
			currentrow.clear();
		}
	}
	return true;
}

/*
    Function: moveVehicle
    Description: Takes a vehicle, and a direction and moves the vehicle.
    Parameters: Pointer to vehicle, short
    Returns: Nothing
*/ 
void Board::moveVehicle(Vehicle *v, short direction)
{
	short leftbehind;
	short x;
	short y;
	//Check just to make sure this vehicle can actually be moved
	if(canMove(v).size() <= 1)
		return;
	
	if(v->getOrientation() == RIGHTLEFT)
	{
		y = v->getOccupying()[0].y;
		if(direction > 0)
		{
			leftbehind = m_spaces.size()+2;
			for(int i=0; i<v->getSize(); i++)
			{
				m_spaces[y][v->getOccupying()[i].x + 1] = v->getDisplay();
				leftbehind = (v->getOccupying()[i].x < leftbehind)?(v->getOccupying()[i].x) : (leftbehind);
			}
			v->changeX(1);
		}
		else
		{
			leftbehind = -1;
			for(int i=0; i<v->getSize(); i++)
			{
				m_spaces[y][v->getOccupying()[i].x - 1] = v->getDisplay();
				leftbehind = (v->getOccupying()[i].x > leftbehind)?(v->getOccupying()[i].x) : (leftbehind);
			}
			v->changeX(-1);
		}
		m_spaces[y][leftbehind] = '.';
	}
	else
	{
		x = v->getOccupying()[0].x;
		if(direction > 0)
		{
			leftbehind = m_spaces.size()+2;
			for(int i=0; i<v->getSize(); i++)
			{
				m_spaces[v->getOccupying()[i].y + 1][x] = v->getDisplay();
				leftbehind = (v->getOccupying()[i].y < leftbehind)?(v->getOccupying()[i].y) : (leftbehind);
			}
			v->changeY(1);
		}
		else
		{
			leftbehind = -1;
			for(int i=0; i<v->getSize(); i++)
			{
				m_spaces[v->getOccupying()[i].y - 1][x] = v->getDisplay();
				leftbehind = (v->getOccupying()[i].y > leftbehind)?(v->getOccupying()[i].y) : (leftbehind);
			}
			v->changeY(-1);
		}
		m_spaces[leftbehind][x] = '.';
	}
}

/*
    Function: getDisplay
    Description: Gets a string holding the display for the board
    Parameters: None
    Returns: string
*/ 
string Board::getDisplay()
{
	string out = "";
	
	for(vector<vector<char> >::iterator xt = m_spaces.begin(); xt != m_spaces.end(); xt++)
	{
		for(vector<char>::iterator yt = xt->begin(); yt != xt->end(); yt++)
		{
			out += (*yt);
		}
		out += "\n";
	}
	return out;
}

/*
    Function: getSize
    Description: Returns the size of the board.
    Parameters: None
    Returns: short
*/ 
short Board::getSize() const
{
	return m_spaces.size() - 1;
}


/*
    Function: getVehicles
    Description: Takes the current gameboard, and builds a vector of vehicles.
    Parameters: None
    Returns: vector a pointers to Vehicles.
*/ 
vector<Vehicle*> Board::getVehicles()
{
	list<char> alreadyfound;
	vector<Vehicle*> vehics;
	Orientation orient;
	bool escape = false;
	short size = 0;
	vector<Coord> coords;
	//We're not looking for - or .: These are not vehicles.
	alreadyfound.push_back('-');
	alreadyfound.push_back('.');
	for(int i = 0; i < m_spaces.size(); i++)
	{
		for(int j = 0; j < m_spaces.size(); j++)
		{
			//Check to see if this space is occupied by a vehicle we've already found.
			if(find(alreadyfound.begin(), alreadyfound.end(), m_spaces[i][j]) == alreadyfound.end())
			{
				//If not, make it so.
				alreadyfound.push_back(m_spaces[i][j]);

				//Check to see if this is an escape car
				if(m_spaces[i][j] == '?') escape = true;
				//We've found 1 occupied space by this car
				size = 1;
				coords.push_back(Coord(j, i));
				//Find the rest of the occupied spaces by this car.
				if(i > 0 && m_spaces[i-1][j] == m_spaces[i][j])
				{
					coords.push_back(Coord(j, i-1));
					size++;
					if(i > 1 && m_spaces[i-2][j] == m_spaces[i][j])
					{
						size++;
						coords.push_back(Coord(j, i-2));
					}
					orient = UPDOWN;
				}
				if(i < m_spaces.size() - 1 && m_spaces[i + 1][j] == m_spaces[i][j])
				{
					coords.push_back(Coord(j, i+1));
					size++;
					if(i < m_spaces.size() - 2 && m_spaces[i+2][j] == m_spaces[i][j])
					{
						size++;
						coords.push_back(Coord(j, i+2));
					}
					orient = UPDOWN;
				}
				if(j > 0 && m_spaces[i][j-1] == m_spaces[i][j])
				{
					coords.push_back(Coord(j-1, i));
					size++;
					if(j > 1 && m_spaces[i][j-2] == m_spaces[i][j])
					{
						size++;
						coords.push_back(Coord(j-2, i));
					}
					orient = RIGHTLEFT;
				}
				if(j < m_spaces.size() - 1 && m_spaces[i][j+1] == m_spaces[i][j])
				{
					coords.push_back(Coord(j+1, i));
					size++;
					if(j < m_spaces.size() - 2 && m_spaces[i][j+2] == m_spaces[i][j])
					{
						size++;
						coords.push_back(Coord(j+2, i));
					}
					orient = RIGHTLEFT;
				}
				//Create a new vehicle, and put it into the vector
				vehics.push_back(new Vehicle(m_spaces[i][j], coords, escape, orient));
				escape = false;
				coords.clear();
			}
		}
	}
	return vehics;
}

/*
    Function: isAWin
    Description: Takes the escape car, and sees if it's position renders this state
		 a win state.
    Parameters: Pointer to a vehicle
    Returns: true if it's in a win state, false otherwise
*/ 
bool Board::isAWin(Vehicle* escape)
{
	for(int i=0; i<escape->getSize(); i++)
	{
		if(escape->getOccupying()[i].x >= m_spaces.size())
			return true;
	}
	return false;
}
