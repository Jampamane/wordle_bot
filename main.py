import time
from multiprocessing import Process
from wordle import Wordle
from multi_process_wordle import PlaySixteen


def main():
    PlaySixteen(number_of_times=1)

if __name__ == "__main__":
    main()
