#include "vehicle.h"

Vehicle::Vehicle()
{
}

Vehicle::Vehicle(const char dis, const vector<Coord> occ, const bool esc, const Orientation orient)
		: m_display(dis), m_spacesoccupying(occ), m_escapable(esc), m_orientation(orient)
{
}

bool Vehicle::isEscapable() const
{
	return m_escapable;
}

vector<Coord> Vehicle::getOccupying() const
{
	return m_spacesoccupying;
}

char Vehicle::getDisplay() const
{
	return m_display;
}

Orientation Vehicle::getOrientation() const
{
	return m_orientation;
}

int Vehicle::getSize() const
{
	return m_spacesoccupying.size();
}

int Vehicle::changeX(const short amt)
{
	for(int i=0; i<m_spacesoccupying.size(); i++)
	{
		m_spacesoccupying[i].x += amt;
	}
}

int Vehicle::changeY(const short amt)
{
	for(int i=0; i<m_spacesoccupying.size(); i++)
	{
		m_spacesoccupying[i].y += amt;
	}
}
