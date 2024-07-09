"""Main function that handles creating an instance and solving wordle."""
import os
from datetime import date
from wordle import Wordle
from rich.console import Console


def main():
    """Create a wordle class and calls the solve method."""
    # Solve wordle
    wordle = Wordle(headless=True)
    wordle.solve()

    # Output to an rst file
    ABSOLUTE_PATH = os.path.dirname(__file__)
    with open(os.path.join(ABSOLUTE_PATH, "docs/source/final_table.rst"), "w", encoding="utf-8") as file:
        final_table = Console(file=file)
        today = date.today()
        final_table.print(f"Today's date: {today}")
        final_table.print(wordle.build_final_table())
        final_table.print(f"Today's wordle is: {wordle.wordle_today.upper()}")


if __name__ == "__main__":
    main()
