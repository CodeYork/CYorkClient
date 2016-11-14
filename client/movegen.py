"""
Move generator class.
"""

import abc
from yourcode import my_move


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
        Run students' AI.
        """
        return my_move(state)


class MoveGeneratorPlayer(MoveGenerator):
    """
    Move generator that takes user input.
    """

    def make_move(self, state):
        return int(input("Enter the column you want: "))

