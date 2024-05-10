from rich.console import Console
from wordle import Wordle
from datetime import datetime


def main():
    console = Console(record=True)
    wordle = Wordle(headless=True)
    console.print("\n")
    if wordle.solve() == True:
        console.clear()
        console.print(wordle._build_table())
        console.print(f"\n- Today's wordle is:  [green bold]{wordle.wordle_today.upper()}[/green bold] -\n")

    with open("wordle.html", "wt") as file:
        file.write(console.export_html())

if __name__ == "__main__":
    main()
