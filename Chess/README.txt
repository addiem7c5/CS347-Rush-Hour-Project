--The Quick How Too--

Choose a language: C++, Java, Python

Open the client/ folder, then open your language of choice (note, c means c++ here).

The only file you should need to change in the provided code is the AI class (AI.h AI.cpp, AI.java, AI.py).

The AI class inherits from BaseAI, which contains everything your program needs to know about, such as:
 * List of pieces representing the current board state
 * List of moves, ordered from most recently made to least recently made
 * Both Players Times
 * If you are player 0 or 1 (White or Black)


 
All languages compile using a provided Makefile.  Any additional files you include will automatically be built
as long as they are in the same directory.

Before playing a game, you must start a game server.  To do so:
  Change directory to the server/ folder
  Run "python main.py"
  *NOTE* this requires libraries that should be on all campus machines.  Also, each computer can only handle a 
    single server, so if one is already running on that computer, just use theirs
    
To start a game, from the same directory as your client
  ./run <hostname>
  where <hostname> is the name of the computer your server is on IE
  ./run rc08xcs213.managed.mst.edu
  This will connect the White player and tell you what game number you just started
  
To join a game, from the same directory as your client
  ./run <hostname> <game> 
  where <hostname> is the name of the computer your server is on, and <game> is the game you are joining IE
  ./run rc08xcs213.managed.mst.edu 7
  This will connect the Black player to game 7, and the game will start
  


