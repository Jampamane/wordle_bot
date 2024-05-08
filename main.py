import time
from wordle import Wordle


def main():
    wordle = Wordle(headless=True)
    wordle.solve()

if __name__ == "__main__":
    while True:
        main()
