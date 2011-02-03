/*  File: vehicle.h
    Author: Addie Martin
    This is the file that defines the class that holds information for 
    a vehicle.
*/
#ifndef VEHICLE_H
#define VEHICLE_H
#include <vector>
#include "types.h"
using namespace std;

/*  Class: Vehicle
    Description: The vehicle class gives us access to useful information pertaining to a 
                 vehicle in the Rush Hour game. It's orientation, display character,
                 the spaces it occupies, and whether or not it is an escape car is
                 specified.
*/
class Vehicle
{
	private:
		Orientation m_orientation;
		char m_display;
		vector<Coord> m_spacesoccupying;
		bool m_escapable;
	public:
		Vehicle();
		Vehicle(const char dis, const vector<Coord> occ, const bool esc, const Orientation orient);
		bool isEscapable() const;
		vector<Coord> getOccupying() const;
		char getDisplay() const;
		Orientation getOrientation() const;
		int getSize() const;
		int changeX(const short amt);
		int changeY(const short amt);
};
#endif
