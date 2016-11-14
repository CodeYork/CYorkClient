import client
import random
import sys


def main(args):
    """
    Instantiate app.
    """
    if len(args) > 1 and args[1] == '--player':
        movegen = client.MoveGeneratorPlayer()
    else:
        movegen = client.MoveGeneratorAI()
    app = client.Client(movegen)
    app.run()


if __name__ == "__main__":
    main(sys.argv)



def my_move(state):
    """
    Put your Connect 4 decision logic in here.

    Args:
        state (list): List of rows in game board, ie. the 'state' of the game.
        Element of a row is True if your token, False if opponent's, and None if empty.

    Returns:
        int: Integer index of column to drop next token into.
    """
    # An example program to choose a random column for your move.
    num_columns = len(state[0])
    chosen_column = random.randint(0, num_columns)

    return chosen_column

