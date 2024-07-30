"""Main function that handles creating an instance and solving wordle."""

from argparse import ArgumentParser
from wordle import Wordle
from output_file import output_file


def main(export):
    """Create a wordle class and calls the solve method."""
    # Solve wordle
    wordle = Wordle(headless=True)
    wordle.solve()

    if export is True:
        # Output to rst file
        output_file(wordle=wordle)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--export", default=False, action="store_true")
    args = parser.parse_args()
    main(export=args.export)
