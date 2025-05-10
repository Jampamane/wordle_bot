"""Main function that handles creating an instance and solving wordle."""

from .wordle import Wordle
from .output_file import output_file
import os


def solve(first_guess: str = "") -> None:
    """
    Solve the wordle by selecting random 'best guesses'.

        Args:
            first_guess (str, optional):
                The first guess the wordle solver will use.
                If blank, will just pick a random word. Defaults to "".

        Raises:
            ValueError:
                Will raise a ValueError if provided an invalid first guess.

    """
    # Solve wordle
    for _ in range(5):  # Attempts to solve wordle 5 times in case it fails
        wordle = Wordle(headless=True)
        solved = wordle.solve(first_guess=first_guess)
        if solved is True:
            break

    if os.getenv("$GITHUB_WORKSPACE"):
        print("Looks like you're running this on GitHub!")
        output_file(wordle)



if __name__ == "__main__":
    solve()