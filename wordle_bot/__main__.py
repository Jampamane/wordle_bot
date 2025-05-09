"""Main function that handles creating an instance and solving wordle."""

from .wordle import Wordle


def solve(first_guess: str = "") -> str:
    """
    Solve the wordle by selecting random 'best guesses'.

        Args:
            first_guess (str, optional):
                The first guess the wordle solver will use.
                If blank, will just pick a random word. Defaults to "".

        Raises:
            ValueError:
                Will raise a ValueError if provided an invalid first guess.

        Returns:
            wordle_today (str): Today's wordle.
    """
    # Solve wordle
    for _ in range(5):  # Attempts to solve wordle 5 times in case it fails
        wordle = Wordle(headless=True)
        solved = wordle.solve(first_guess=first_guess)
        if solved is True:
            break

    return wordle.wordle_today


if __name__ == "__main__":
    solve()