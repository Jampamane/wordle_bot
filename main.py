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
    with open(os.path.join(ABSOLUTE_PATH, "docs/source/final_table.rst"), "a", encoding="utf-8") as file:
        final_table = Console(file=file)
        today = date.today()
        final_table.print(
            f".. list-table:: Wordle for {today}\n"
            "   :header-rows: 0\n"
            )
        for x in range(1, 7):
            if not len(wordle.wordle["guess"][x]["word"]) == 0:
                final_table.print(
                    f"   * - {wordle.wordle["guess"][x]["word"]}\n"
                    f"   - {wordle.wordle["guess"][x]["letters"][0]}\n"
                    f"   - {wordle.wordle["guess"][x]["letters"][1]}\n"
                    f"   - {wordle.wordle["guess"][x]["letters"][2]}\n"
                    f"   - {wordle.wordle["guess"][x]["letters"][3]}\n"
                    f"   - {wordle.wordle["guess"][x]["letters"][4]}\n"
                )
            else:
                final_table.print(
                    f"   * - \n"
                    f"   - \n"
                    f"   - \n"
                    f"   - \n"
                    f"   - \n"
                    f"   - \n"
                )
        
        final_table.print(f"Today's wordle is: {wordle.wordle_today.upper()}")


if __name__ == "__main__":
    main()
