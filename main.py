"""Main function that handles creating an instance and solving wordle."""
from wordle import Wordle


def main():
    """Create a wordle class and calls the solve method."""
    wordle = Wordle(headless=True)
    wordle.solve()


if __name__ == "__main__":
    main()
