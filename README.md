#Code York Client

This software acts as the client code run on each student's computer.

It has an empty region in the code for students to write their software.

NB: It holds code for the Connect 4 game at the moment.


##HTTP interface

The following HTTP interface is used:

* post /game : Make a new game.
* post /game/[id]/join : Join a game with 'id'.
* post /game/[id]/start : Start the game.
* get /game/[id]/state : Get the game state.
* post /game/[id]/move : Make a player move.


