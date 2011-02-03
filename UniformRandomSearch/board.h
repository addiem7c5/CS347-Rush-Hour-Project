/*  File: board.h
    Author: Addie Martin
    This is the file that defines the board. 
*/
#ifndef BOARD_H
#define BOARD_H
#include <vector>
#include <string>
#include "types.h"
#include "vehicle.h"
using namespace std;

/*
  Class: Board
  Description: This class has all of the state generation 
	       methods for each state. Since 'Board' itself
	       holds a state of the game, this lets us look 
               at exactly what that state looks like.
*/ 
class Board
{
	private:
		vector<vector<char> > m_spaces;
	public:
		Board();
		Board(const Board& b);
		vector<short> canMove(Vehicle *v);
		bool loadBoard(string filename);
		void moveVehicle(Vehicle *v, short direction);
		string getDisplay();
		short getSize() const;
		vector<Vehicle*> getVehicles();
		bool isAWin(Vehicle* v);
};
#endif
