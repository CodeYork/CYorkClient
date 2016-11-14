"""
Put all of your code in this file!
"""

import random


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
    chosen_column = random.randint(num_columns)

    return chosen_column

