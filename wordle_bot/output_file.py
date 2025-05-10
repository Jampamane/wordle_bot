import os
from rich.console import Console
from datetime import date
from wordle_bot.wordle import Wordle


def output_file(wordle: Wordle) -> None:
    """Plays wordle, then exports wordle to docs/final_table.md.

    Args:
        wordle (Wordle):
            Wordle object used for the data in exporting.
    """

    FINAL_TABLE_ABSOLUTE_PATH = os.path.join(os.getenv("GITHUB_WORKSPACE"), "docs/final_table.md")
    with open(
        FINAL_TABLE_ABSOLUTE_PATH,
        "a",
        encoding="utf-8",
    ) as file:
        final_table = Console(file=file)
        today = date.today()
        final_table.print(
            "|   |   |   |   |   |   |"
            + "\n"
            + "| - | - | - | - | - | - |"
        )
        for x in range(1, 7):
            if not len(wordle.wordle["guess"][x]["word"]) == 0:
                final_table.print(
                    f"| {wordle.wordle["guess"][x]["word"].capitalize()}" +
                    f" | {wordle.wordle["guess"][x]["letters"][1][0]}" +
                    f" | {wordle.wordle["guess"][x]["letters"][2][0]}" +
                    f" | {wordle.wordle["guess"][x]["letters"][3][0]}" +
                    f" | {wordle.wordle["guess"][x]["letters"][4][0]}" +
                    f" | {wordle.wordle["guess"][x]["letters"][5][0]} |"
                )
            else:
                final_table.print(
                    "|   |   |   |   |   |   |"
                )

        final_table.print(f"The Wordle for {today} is: {wordle.wordle_today.upper()}")
