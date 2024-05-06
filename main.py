from wordle import Wordle
from multiprocessing import Process


def main():
    wordle = Wordle()
    wordle.solve(mode="easy")


if __name__ == "__main__":
    main()