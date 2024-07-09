import os
from rich.console import Console
from datetime import date
from wordle import Wordle

def output_file(wordle: Wordle):
    ABSOLUTE_PATH = os.path.dirname(__file__)
    with open(os.path.join(ABSOLUTE_PATH, "docs/source/final_table.rst"), "a", encoding="utf-8") as file:
        final_table = Console(file=file)
        today = date.today()
        final_table.print(
            ".. list-table:: Wordle for " + str(today) + "\n" +
            "   :widths: 10 3 3 3 3 3\n" +
            "   :header-rows: 0\n"
            )
        for x in range(1, 7):
            if not len(wordle.wordle["guess"][x]["word"]) == 0:
                final_table.print(
                    "   * - " + wordle.wordle["guess"][x]["word"].capitalize() + "\n" +
                    "     - " + wordle.wordle["guess"][x]["letters"][0][0] + "\n" +
                    "     - " + wordle.wordle["guess"][x]["letters"][1][0] + "\n" +
                    "     - " + wordle.wordle["guess"][x]["letters"][2][0] + "\n" +
                    "     - " + wordle.wordle["guess"][x]["letters"][3][0] + "\n" +
                    "     - " + wordle.wordle["guess"][x]["letters"][4][0]
                )
            else:
                final_table.print(
                    "   * - \n" +
                    "     - \n" +
                    "     - \n" +
                    "     - \n" +
                    "     - \n" +
                    "     -"
                )
        
        final_table.print(f"Today's wordle is: {wordle.wordle_today.upper()}")