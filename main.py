"""Main function that handles creating an instance and solving wordle."""

from wordle import Wordle
from output_file import output_file


def main():
    """Create a wordle class and calls the solve method."""
    # Solve wordle
    wordle = Wordle(headless=True)
    wordle.solve()

    # Output to rst file
    output_file(wordle=wordle)


if __name__ == "__main__":
    main()
