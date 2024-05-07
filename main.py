from wordle import Wordle
from multiprocessing import Process


def main():
    wordle = Wordle()
    wordle.solve()


if __name__ == "__main__":
    main()
    '''
    one = Process(target=main)
    two = Process(target=main)
    three = Process(target=main)
    four = Process(target=main)
    one.start()
    two.start()
    three.start()
    four.start()
    one.join()
    two.join()
    three.join()
    four.join()
    '''
