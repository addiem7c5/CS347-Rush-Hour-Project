/*  File: main.cpp
    Author: Addie Martin
    This is the main file where the Uniform Random Search does its
    business. It takes the initial state of the board, finds the
    vehicles that can move, which essentially generates all the next
    possible states and randomly chooses one to go to. All of these
    states are pusehd onto a queue, for viewing after the algorithm
    is finished.
*/

#include "vehicle.h"
#include "board.h"
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <queue>

using namespace std;

int main(int argc, char** argv)
{
	//Needed Declarations
	string input;
	vector<VehicleMovement> canmove;
	queue<Board*> solution;
	Vehicle* escapecar;
	vector<Vehicle*> vehicles;
	Board* currentstate = new Board();
	int moving = 0;

	srand(time(NULL));
	
	//Take board file name from command line if possible.
	if(argc > 1)
	{
		if(!currentstate->loadBoard(string(argv[1])))
		{	
			cout<<argv[1]<<" could not be loaded!"<<endl;
			return 1;
		}
	}
	else
	{
		cout<<"What board would you like to load?"<<endl;
		cin>>input;
		if(!currentstate->loadBoard(input))
		{
			cout<<input<<" could not be loaded!"<<endl;
			return 1;
		}
	}
	//Output what the board looks like in its inital state
	cout<<currentstate->getDisplay();

	//Get all of the vehicles from the board and see which
	//is the escape car.
	vehicles = currentstate->getVehicles();
	for(vector<Vehicle*>::iterator i = vehicles.begin(); i != vehicles.end(); i++)
	{
		if((*i)->isEscapable()) escapecar = *i;
	}

	//Algorithm loop, checks if the current state is a win position
	while(currentstate->isAWin(escapecar) == false)
	{
		//Pushes the current state into the solution
		solution.push(currentstate);

		//Finds all the vehicles that can move in the current state
		for(vector<Vehicle*>::iterator i = vehicles.begin(); i != vehicles.end(); i++)
		{
			if(currentstate->canMove(*i).size() > 1)
			{
				for(int j=1; j<currentstate->canMove(*i).size(); j++)
				{
					canmove.push_back(VehicleMovement((*i), currentstate->canMove(*i)[j]));
				}
			}
		}

		//Generate a random number that is less than the number
		//of movable vehicles. This is to be used as an index.
		moving = rand()%canmove.size();

		//Since the current state was already pusehd onto the solution
		//we need to release its pointer, and create new data for the
		//next state (now the current state)
		currentstate = NULL;
		currentstate = new Board(*(solution.back()));
		//We move the randomly chosen vehicle in this new state.
		currentstate->moveVehicle(canmove[moving].v, canmove[moving].m);
		//Clear the possibly moved vehicles for the next iteration.
		canmove.clear();
	}
	//Have to push the winning state onto the solution
	solution.push(currentstate);

	
	cout<<"Using "<<solution.size()<<" states."<<endl;
	cout<<"Press any key to continue..."<<endl;
	cin.get();
	cout<<"The moves that generate a goal state in succession are: "<<endl;
	//Output solution states to screen
	while(!solution.empty())
	{
		cout<<solution.front()->getDisplay()<<endl;
		delete solution.front();
		solution.pop();
	}

	//Clean Up Memory
	for(int i=0; i < vehicles.size(); i++)
	{
		delete vehicles[i];
	}

	return 0;
	
}

