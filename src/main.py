"""Main function that handles creating an instance and solving wordle."""

from argparse import ArgumentParser
from wordle import Wordle
from output_file import output_file


def main(export: bool) -> None:
    """
    Create a wordle class and calls the solve method.

    Args:
        export (bool):
            Bool that determines weather to export Wordle to docs/source/final_table.rst.
            Defaults to False.
            Can specify True when calling main function from the command line with --export.
            Example: python wordle_bot/src/main.py --export
    """
    # Solve wordle
    for _ in range(5): # Attempts to solve wordle 5 times in case it fails
        wordle = Wordle(headless=False)
        solved = wordle.solve()
        if solved is True:
            break

    if export is True:
        # Output to rst file
        output_file(wordle=wordle)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--export", default=False, action="store_true")
    args = parser.parse_args()
    main(export=args.export)
