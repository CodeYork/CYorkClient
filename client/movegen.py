"""
Move generator class.
"""

import abc


class MoveGenerator(object, metaclass=abc.ABCMeta):
    """
    Generator of Connect 4 moves.
    """

    @abc.abstractmethod
    def make_move(self, state):
        """
        Make a move based on game state.

        Args:
            state (list[list[bool]]): List of columns of board.
                True if player's token, False if enemies, None if no token.

        Returns:
            int: Index of column to place token in.
        """


class MoveGeneratorAI(MoveGenerator):
    """
    Automated move generator.
    """

    def make_move(self, state):
        """
        Paste your code in here! Make sure to indent with 8 spaces.

        (The code in here right now is a stand-in that chooses a random
        column. Can you see how this works?)
        """
        return random.randint(0, len(state)-1)


class MoveGeneratorPlayer(MoveGenerator):
    """
    Move generator that takes user input.
    """

    def make_move(self, state):
        """
        Print state to screen and ask for a column to drop token into.

        WARNING: Messy string manipulations ahead. Don't worry if you can't read it,
        but trying to understand it is always a big plus!
        """
        return int(input("Enter the column you want: "))

