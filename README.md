#Code York Client

This software acts as the client code run on each student's computer.

It has an empty region in the code for students to write their software.

NB: It holds code for the Connect 4 game at the moment.


##HTTP interface

The following HTTP interface is used:

* POST /game : Make a new game.
* POST /game/[id]/join : Join a game with 'id'.
* POST /game/[id]/start : Start the game.
* GET /game/[id] : Get the game state.
* POST /game/[id]/move : Make a player move.


